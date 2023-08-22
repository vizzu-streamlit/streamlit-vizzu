import pandas as pd
import streamlit as st
from ipyvizzu.animation import Config, Data, Style

from streamlit_vizzu import VizzuChart

data_frame = pd.read_csv(
data_frame = pd.read_csv("football-transfers/football_transfers_cleaned.csv", dtype={"year": str})
#data_frame = pd.read_csv("./football_transfers_cleaned.csv", dtype={"year": str})

data = Data()
data.add_df(data_frame, max_rows=25000)

chart = VizzuChart(key="vizzu", height=600)
chart.animate(data)
chart.feature("tooltip", True)

year = st.slider("Pick a year", min_value=1992, max_value=2022, value=2010)
col1, col2, col3, col4, col5 = st.columns(5)

compare_by = col1.radio("Compare by", ["Fees earned", "Fees spent", "Balance"], index=2)
if compare_by == "Fees earned":
	compare_title = "Transfer fees earned in "
	x = "fee[m€]"
	filter = f"record.year <= '{year}' && record.transfer_movement == 'out'"
elif compare_by == "Fees spent":
	compare_title = "Transfer fees spent in "
	x = "fee[m€]"
	filter = f"record.year <= '{year}' && record.transfer_movement == 'in'"
else:
	compare_title = "Balance of transfer fees in "
	x = "fee_real[m€]"
	filter = f"record.year <= '{year}'" 
	
order_by = col2.radio("Order by", ["Value","Alphabet"])
if order_by == "Value":
	sort = "byValue"
else:
	sort = "none"


chart.animate(
    Data.filter(filter),
    Config(
        {"x": x, 
		"y": "club_name", 
		"color": "club_name",
		"label": x,
		"sort": sort,
		"title": f"{compare_title}{year}"}
    ),
    Style(
        {
            "plot": {
                "xAxis": {"label": {"numberScale": "shortScaleSymbolUS"}},
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
    delay = 0,
	#duration=0.2,
    x={"easing": "linear", "delay": 0},
    y={"delay": 0},
    show={"delay": 0},
    hide={"delay": 0},
    title={"duration": 0, "delay": 0},
)

chart.show()
