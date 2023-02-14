# streamlit-vizzu

Bidirectional streamlit component for interacting with [vizzu](https://vizzuhq.com/)
animations. This package builds on the excellent
[ipyvizzu](https://github.com/vizzuhq/ipyvizzu) library and adds some streamlit-specific
code to allow you to interact with an ipyvizzu chart within a streamlit app without
the chart being redrawn on every interaction.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://blackary-streamlit-vizzu-example-app1-1ks8b0.streamlit.app/)

## Installation instructions

```sh
pip install streamlit-vizzu
```

## Usage instructions

```python
import pandas as pd
import streamlit as st
from ipyvizzu.animation import Config, Data
from ipyvizzu.chart import Chart

from streamlit_vizzu import VizzuChart

data_frame = pd.read_csv(
    "https://raw.githubusercontent.com/vizzuhq/ipyvizzu/main/docs/examples/stories/titanic/titanic.csv"
)
data = Data()
data.add_data_frame(data_frame)

# Must pass display="manual" to Chart constructor
chart = Chart(width="640px", height="360px", display="manual")

chart.animate(data)
chart.animate(
    Config(
        {
            "x": "Count",
            "y": "Sex",
            "label": "Count",
            "title": "Passengers of the Titanic",
            "color": "Sex",
        }
    )
)

vchart = VizzuChart(chart)

if st.checkbox("Show survival rates"):
    vchart.animate(
        Config(
            {
                "x": ["Count", "Survived"],
                "label": ["Count", "Survived"],
                "color": "Survived",
            }
        )
    )
    vchart.animate(Config({"x": "Count", "y": ["Sex", "Survived"]}))

value = vchart.show()

# See if the user clicks on the chart
st.write(value)
```
