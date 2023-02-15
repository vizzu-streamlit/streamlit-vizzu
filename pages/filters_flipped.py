import pandas as pd
import streamlit as st
from ipyvizzu.animation import Config, Data, Style

from streamlit_vizzu import VizzuChart as Chart

data_frame = pd.read_csv("pages/sales.csv")
data = Data()
data.add_data_frame(data_frame)

chart = Chart(height=360)

chart.animate(data)
chart.feature("tooltip", True)

bg_color = st.session_state.get("bg_color", "#fff")
items = st.session_state.get("items", ["Shoes", "Handbags", "Gloves", "Accessories"])
measure = st.session_state.get("measure", "Sales")
compare_by = st.session_state.get("compare_by", "Region")
coords = st.session_state.get("coords", "Cartesian")
order = st.session_state.get("order", "By value")

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

chart.animate(Data.filter(filter), Config(config), style, delay=0.1)
output = chart.show()

items: list[str] = st.multiselect(
    "Products",
    ["Shoes", "Handbags", "Gloves", "Accessories"],
    ["Shoes", "Handbags", "Gloves", "Accessories"],
    key="items",
)

col1, col2, col3, col4, col5 = st.columns(5)

measure: str = col1.radio("Measure", ["Sales", "Revenue [$]"], key="measure")  # type: ignore
compare_by = col2.radio("Compare by", ["Region", "Product", "Both"], key="compare_by")
coords = col3.radio(
    "Coordinate system", ["Cartesian (desktop)", "Polar (mobile)"], key="coords"
)
order = col4.radio("Order items", ["Alphabetically", "By value"], key="order")

bg_color = col5.color_picker("Background color", "#fff", key="bg_color")
