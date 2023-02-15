import pandas as pd
from ipyvizzu.animation import Config, Data

from streamlit_vizzu import VizzuChart

chart = VizzuChart(rerun_on_click=True, default_duration=1)

df = pd.DataFrame(
    {
        "a": ["x", "y", "z", "x", "y", "z"],
        "b": [1, 2, 3, 4, 5, 6],
        "c": ["A", "A", "B", "B", "C", "D"],
    }
)

data = Data()
data.add_data_frame(df)
chart.animate(data)

bar_clicked = chart.get("marker.categories.a")

if bar_clicked is None:
    chart.animate(Data.filter())
    chart.animate(
        Config({"x": "a", "y": "b", "title": "Look at my plot! Click!", "color": None}),
    )
else:
    chart.animate(Data.filter(f"record['a'] == '{bar_clicked}'"))
    chart.animate(
        Config(
            {
                "x": "c",
                "y": "b",
                "title": f"Drilldown for a = {bar_clicked}",
                "color": "c",
            }
        )
    )

chart.show()
