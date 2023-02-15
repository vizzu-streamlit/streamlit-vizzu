import pandas as pd
from ipyvizzu.animation import Config, Data

from streamlit_vizzu import VizzuChart

chart = VizzuChart()

df = pd.DataFrame({"a": ["x", "y", "z"], "b": [1, 2, 3]})

data = Data()
data.add_data_frame(df)
chart.animate(data)
chart.animate(Config({"x": "a", "y": "b", "title": "Look at my plot!"}))

import streamlit as st

if st.checkbox("Swap"):
    chart.animate(Config({"y": "a", "x": "b", "title": "Swapped!"}))

chart.show()
