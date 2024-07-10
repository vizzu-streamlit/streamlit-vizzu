from __future__ import annotations

from pathlib import Path
from typing import Any
from importlib.metadata import version
from distutils.version import StrictVersion
import uuid

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
        width: int | str = 700,
        height: int | str = 480,
        key: str = "vizzu",
        return_clicks: bool = True,
        rerun_on_click: bool = False,
        default_duration: float | None = None,
        use_container_width: bool = False,
        **kwargs,
    ):
        """
        Create a VizzuChart object for use in a streamlit app

        width: specify width of chart in pixels
        height: specify height of chart in pixels
        key: specify unique key for chart, defaults to `vizzu`
        return_clicks: specify whether or not the chart should return values \
            when clicked
        rerun_on_click: if True, and return_clicks is True, will call \
            st.experimental_rerun() whenever your chart is clicked
        default_duration: specify the default duration that will be applied to all \
            animations, in seconds
        """
        self.key = key
        self.div_id = f"{self.key}_vizzu"
        self.chart_id = f"{self.key}_vizzu_chart"
        self.animations: list[str] = []
        self.return_clicks = return_clicks
        self.height = height
        self.rerun_on_click = rerun_on_click
        self.default_duration = default_duration
        self.ipyvizzu_version = StrictVersion(version("ipyvizzu"))

        if use_container_width:
            _width = "100%"
        elif isinstance(width, int):
            _width = f"{width}px"
        else:
            _width = width

        if isinstance(height, int):
            _height = f"{height - 20}px"  # account for padding
        else:
            _height = height

        super().__init__(
            width=_width,
            height=_height,
            display=DisplayTarget.MANUAL,
            **kwargs,
        )

        if self.ipyvizzu_version >= StrictVersion("0.15.0"):
            self.initializing()

    def show(self):
        """
        Render your chart within your streamlit app. Note that any animations
        applied after your chart is shown will not affect the chart.
        """
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
        click (e.g. "target.categories.a").
        If there hasn't been a click, or that path isn't found, return
        the default value.
        """
        try:
            val: Any = self
            for sub_key in dotted_key.split("."):
                val = val[sub_key]
            return val
        except (KeyError, TypeError):
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

    def _animation_to_js(self, *animations: Any, **options: Any):
        if self.ipyvizzu_version < StrictVersion("0.15.0"):
            animation = self._merge_animations(animations)
            animate = Animate(animation, options)
            return DisplayTemplate.ANIMATE.format(
                display_target=self._display_target.value,
                chart_id=self._chart_id,
                scroll=str(self._scroll_into_view).lower(),
                **animate.dump(),
            )

        from ipyvizzu.animation import AnimationMerger

        animation = AnimationMerger.merge_animations(animations)
        animate = Animate(animation, options)
        self._last_anim = uuid.uuid4().hex[:7]
        return DisplayTemplate.ANIMATE.format(
            display_target=self._display_target.value,
            chart_id=self._chart_id,
            anim_id=self._last_anim,
            scroll=str(self._scroll_into_view).lower(),
            **animate.dump(),
        )

    def animate(self, *animations: Any, **options: Any):
        """
        Pass any number of Animation objects (e.g. Data, Config, or Style objects), and
        any options that should be applied to them.
        """
        if self.default_duration and "duration" not in options:
            options["duration"] = self.default_duration
        js = self._animation_to_js(*animations, **options)
        js = js.replace("(element,", f"(document.getElementById('{self.div_id}'),")
        self.animations.append(js)
