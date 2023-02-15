from __future__ import annotations

from pathlib import Path
from typing import Any

import streamlit as st
import streamlit.components.v1 as components
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
        width: int = 700,
        height: int = 480,
        key: str | None = None,
        return_clicks: bool = True,
        rerun_on_click: bool = False,
        default_duration: float | None = None,
        **kwargs,
    ):
        self.key = key or "vizzu"
        self.div_id = f"{self.key}_vizzu"
        self.chart_id = f"{self.key}_vizzu_chart"
        self.animations: list[str] = []
        self.return_clicks = return_clicks
        self.height = height
        self.chart_height = height - 20
        self.rerun_on_click = rerun_on_click
        self.default_duration = default_duration

        super().__init__(
            width=f"{width}px",
            height=f"{self.chart_height}px",
            display=DisplayTarget.MANUAL,
            **kwargs,
        )

        self._chart_id

    def show(self):
        component_value = _component_func(
            div_id=self.div_id,
            chart_id=self.chart_id,
            script=self._get_script(),
            return_clicks=self.return_clicks,
            key=self.key,
            height=self.height,
        )

        if component_value != st.session_state[self.key] and self.rerun_on_click:
            st.experimental_rerun()

        return component_value

    def __getitem__(self, key: str) -> dict:
        """
        Use the chart like a dictionary, but the caller should handle cases where
        there hasn't been a click yet, or the key isn't found by handling TypeError
        and/or KeyError
        """
        return st.session_state[self.key][key]

    def get(self, dotted_key: str, default: Any = None) -> Any:
        """
        Pass a dot-separated key to access a specific value from the latest
        click (e.g. "marker.categories.a").
        If there hasn't been a click, or that path isn't found, return
        the default value.
        """
        try:
            val = self
            for sub_key in dotted_key.split("."):
                val = val[sub_key]
            return val
        except (KeyError, ValueError):
            return default

    def _get_script(self) -> str:
        script = (
            self._calls[0]
            + "\n"
            + "\n".join(self._calls[1:]).replace(
                "element", f'document.getElementById("{self.div_id}")'
            )
        )
        script += "\n".join(self.animations)
        raw_chart_id = self._chart_id

        script = script.replace(raw_chart_id, self.chart_id)

        return script

    def _repr_html_(self) -> str:
        return f'<div id="{self.chart_id}"><script>{self._get_script()}</script></div>'

    def animation_to_js(self, *animations: Any, **options: Any):
        animation = self._merge_animations(animations)
        animate = Animate(animation, options)
        return DisplayTemplate.ANIMATE.format(
            display_target=self._display_target.value,
            chart_id=self._chart_id,
            scroll=str(self._scroll_into_view).lower(),
            **animate.dump(),
        )

    def animate(self, *animations: Any, **options: Any):
        if self.default_duration and "duration" not in options:
            options["duration"] = self.default_duration
        js = self.animation_to_js(*animations, **options)
        js = js.replace("(element,", f"(document.getElementById('{self.div_id}'),")
        self.animations.append(js)
