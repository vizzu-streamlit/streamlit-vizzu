from pathlib import Path
from typing import Any, Optional

import streamlit.components.v1 as components
from bs4 import BeautifulSoup
from ipyvizzu.animation import Animation
from ipyvizzu.chart import Chart
from ipyvizzu.method import Animate
from ipyvizzu.template import DisplayTarget, DisplayTemplate

# Tell streamlit that there is a component called streamlit_vizzu,
# and that the code to display that component is in the "frontend" folder
frontend_dir = (Path(__file__).parent / "frontend").absolute()
_component_func = components.declare_component(
    "streamlit_vizzu", path=str(frontend_dir)
)


class VizzuChart(Chart):
    def __init__(
        self,
        # chart: Chart,
        width: int = 800,
        height: int = 480,
        key: Optional[str] = None,
        return_clicks: bool = True,
    ):
        self.key = key or "vizzu"
        self.div_id = f"{self.key}_vizzu"
        self.chart_id = f"{self.key}_vizzu_chart"
        self.animations: list[str] = []
        self.return_clicks = return_clicks
        self.height = height

        super().__init__(
            width=f"{width}px", height=f"{height}px", display=DisplayTarget.MANUAL
        )

    def show(self):
        html = self._repr_html_()
        soup = BeautifulSoup(html, "html.parser")
        raw_div_id: str = soup.find("div").get("id")  # type: ignore
        script = soup.find("script").get_text()  # type: ignore
        script += "\n".join(self.animations)
        raw_chart_id = self._chart_id

        script = script.replace(raw_div_id, self.div_id)
        script = script.replace(raw_chart_id, self.chart_id)

        component_value = _component_func(
            div_id=self.div_id,
            chart_id=self.chart_id,
            script=script,
            return_clicks=self.return_clicks,
            key=self.key,
            height=self.height,
        )

        return component_value

    def _repr_html_(self) -> str:
        html_id = self.chart_id
        script = (
            self._calls[0]
            + "\n"
            + "\n".join(self._calls[1:]).replace(
                "element", f'document.getElementById("{html_id}")'
            )
        )
        return f'<div id="{html_id}"><script>{script}</script></div>'

    def animation_to_js(self, *animations: Animation, **options: Any):
        animation = self._merge_animations(animations)
        animate = Animate(animation, options)
        return DisplayTemplate.ANIMATE.format(
            display_target=self._display_target.value,
            chart_id=self._chart_id,
            scroll=str(self._scroll_into_view).lower(),
            **animate.dump(),
        )

    def animate(self, *animations: Animation, **options: Any):
        js = self.animation_to_js(*animations, **options)
        js = js.replace("(element,", f"(document.getElementById('{self.div_id}'),")
        self.animations.append(js)
