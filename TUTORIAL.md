# Streamlit-Vizzu Tutorial

## Installation

To get started with Streamlit-Vizzu, first you need to install the package

```sh
pip install streamlit-vizzu
```

## Create your first chart

Create a file called `streamlit_app.py` with the following content

```python
from ipyvizzu.chart import Chart
from streamlit_vizzu import VizzuChart

chart = Chart(display="manual")

vchart = VizzuChart(chart)


import pandas as pd
from ipyvizzu import Chart, Data, Config, Style

data_frame = pd.read_csv(
    "https://raw.githubusercontent.com/vizzuhq/ipyvizzu/gh-pages/docs/data/chart_types_eu.csv",
)
data = Data()
data.add_data_frame(data_frame)

chart = Chart()
chart.animate(data)

chart.animate(
    Config.column({"x": "Joy factors", "y": "Value 2 (+)", "title": "Column Chart"}),
    Style(
        {
            "plot": {
                "paddingLeft": "8em",
                "yAxis": {"label": {"paddingRight": "0.8em"}},
                "xAxis": {"label": {"paddingTop": "0.8em"}},
            }
        }
    ),
)

VizzuChart(chart).show()
```
