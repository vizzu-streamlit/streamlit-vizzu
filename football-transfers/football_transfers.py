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

year = st.slider("Pick a year", min_value=1992, max_value=2022, value=2010)
compare_by = st.radio("Compare by", ["Fees earned", "Fees spent", "Balance"], index=2)
if compare_by == "Fees earned":
	compare_title = "Transfer fees earned in "
	x = "fee[m€]"
	filter = f"record.year == '{year}' && record.transfer_movement == 'out'"
elif compare_by == "Fees spent":
	compare_title = "Transfer fees spent in "
	x = "fee[m€]"
	filter = f"record.year == '{year}' && record.transfer_movement == 'in' && record.club_name =='Arsenal FC'"
else:
	compare_title = "Balance of transfer fees in "
	x = "fee_real[m€]"
	filter = f"record.year == '{year}'" 


chart.animate(
    Data.filter(filter),	
    Config(
        {"x": [x,"player_name"], 
		"y": "club_name", 
		"color": "club_name",
		"lightness":"player_name",
		#"sort": "byValue",
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
