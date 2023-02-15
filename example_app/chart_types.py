import pandas as pd
from ipyvizzu import Config, Data, Style

from streamlit_vizzu import VizzuChart as Chart

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

chart.show()
