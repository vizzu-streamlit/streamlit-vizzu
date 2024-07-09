from __future__ import annotations

import pandas as pd
import streamlit as st

from streamlit_vizzu import Config, Data, Style, VizzuChart

data_frame = pd.read_csv("data/sales.csv")
data = Data()
data.add_df(data_frame)

chart = VizzuChart()

chart.animate(data)
chart.feature("tooltip", True)

items: list[str] = st.multiselect(
    "Products",
    ["Shoes", "Handbags", "Gloves", "Accessories"],
    ["Shoes", "Handbags", "Gloves", "Accessories"],
)

col1, col2, col3, col4, col5 = st.columns(5)

measure: str = col1.radio("Measure", ["Sales", "Revenue [$]"])
compare_by = col2.radio("Compare by", ["Product", "Region", "Both"])
coords = col3.radio("Coordinate system", ["Cartesian (desktop)", "Polar (mobile)"])
order = col4.radio("Order items", ["Alphabetically", "By value"])
bg_color = col5.color_picker("Background color", "#fff")

style = Style({"plot": {"backgroundColor": bg_color}})

filter = " || ".join([f"record['Product'] == '{item}'" for item in items])
title = f"{measure} of " + ", ".join(items)

if compare_by == "Product":
    y = ["Product"]
    x = [measure]
    color = None

elif compare_by == "Region":
    y = [measure]
    x = ["Region"]
    color = ["Region"]

else:
    y = ["Product"]
    x = [measure, "Region"]
    color = ["Region"]


config = {
    "title": title,
    "y": y,
    "label": measure,
    "x": x,
    "color": color,
}

if coords == "Polar (mobile)":
    config["coordSystem"] = "polar"
else:
    config["coordSystem"] = "cartesian"

if order == "Alphabetically":
    config["sort"] = "none"
else:
    config["sort"] = "byValue"

chart.animate(Data.filter(filter), Config(config), style, delay=0)
output = chart.show()

st.write("Click on the chart to check the underlying data")

st.write(output)
