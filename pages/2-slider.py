import pandas as pd
import streamlit as st
from ipyvizzu.animation import Config, Data, Style

from streamlit_vizzu import VizzuChart

data_frame = pd.read_csv(
    "data/music.csv", dtype={"Year": str}
)

data = Data()
data.add_data_frame(data_frame)

chart = VizzuChart(key="vizzu", height=380)
chart.animate(data)
chart.feature("tooltip", True)

year = st.slider("Pick a year", min_value=1973, max_value=2021, value=1990)

chart.animate(
	Data.filter("record.Year === year"), 
	Config.groupedBar(
        {
            "x": "Revenue [m$]",
            "y": "Format",
            "groupedBy": "Format",
        }
    ),
    Style({
        "plot": { "marker": { "colorPalette": "#b74c20FF #c47f58FF #1c9761FF #ea4549FF #875792FF #3562b6FF #ee7c34FF #efae3aFF"}},
    }),
	delay='0.1'
)
	
output = chart.show()
