import pandas as pd
import streamlit as st
from ipyvizzu.animation import Config, Data, Style

from streamlit_vizzu import VizzuChart

data_frame = pd.read_csv("football-transfers/football_transfers_cleaned.csv", dtype={"year": str})

data = Data()
data.add_data_frame(data_frame)

chart = VizzuChart(key="vizzu", height=380)
chart.animate(data)
chart.feature("tooltip", True)

year = st.slider("Pick a year", min_value=1992, max_value=2022, value=2020)

compare_title = "Transfer fees spent in "
x = "fee[m€]"
filter = f"record.year == '{year}' && record.transfer_movement == 'in' && record.club_name =='Arsenal FC'"


chart.animate(
    Data.filter(filter),	
    Config(
        {"x": [x,"player_name"], 
		"y": "player_name", 
		"color": "player_name",
		"sort": "byValue",
		"label": x,
		"title": f"{compare_title}{year}"}
    ),
    Style(
        {
            "plot": {
                "xAxis": {
					"label": {
						"numberScale": "shortScaleSymbolUS"}},
                "marker": {
                    "colorPalette": (
                        "#b74c20FF #c47f58FF #1c9761FF #ea4549FF #875792FF #3562b6FF "
                        "#ee7c34FF #efae3aFF"
                    ),
                    "label": {
                        "numberFormat": "prefixed",
                        "maxFractionDigits": "1",
                        "numberScale": "shortScaleSymbolUS",
                    },
                },
                "paddingLeft": "13em",
            }
        }
    ),
    delay="0",
)

chart.show()
