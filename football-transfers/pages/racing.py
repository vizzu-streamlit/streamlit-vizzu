import pandas as pd
import streamlit as st
from ipyvizzu.animation import Config, Data, Style

from streamlit_vizzu import VizzuChart

#data_frame = pd.read_csv("football-transfers/football_transfers_cleaned.csv", dtype={"year": str})
data_frame = pd.read_csv("./football_transfers_cleaned.csv", dtype={"year": str})

data = Data()
data.add_df(data_frame, max_rows=25000)

chart = VizzuChart(key="vizzu", height=600)
chart.animate(data)
chart.feature("tooltip", True)

for y in range(1992, 2022):
	chart.animate(
		Data.filter(f"record.year <= {y} && record.transfer_movement == 'in'"),	
		Config({
			"x": "fee[m€]", 
			"y": {"set":"club_name","range": {"min": "-9.99999max"}}, 		
			#"y":"club_name",
			"color": "club_name",
			"label": "fee[m€]",
			"sort":"byValue",
			"title": f"Transfer fees up to {y}"
			}),
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
		delay = 0,
		duration=0.4,
		x={"easing": "linear", "delay": 0},
		y={"delay": 0},
		show={"delay": 0},
		hide={"delay": 0},
		title={"duration": 0, "delay": 0},
	)

chart.show()
