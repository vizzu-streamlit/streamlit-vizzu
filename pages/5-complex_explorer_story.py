from typing import List
import pandas as pd
import streamlit as st
import numpy as np
from ipyvizzu.animation import Config, Data, Style
from ipyvizzustory.env.py.story import Story
from ipyvizzustory import Step, Slide

from streamlit_vizzu import VizzuChart

data_frame = pd.read_csv("data/music2.csv", dtype={"Year": str})

data = Data()
data.add_data_frame(data_frame)

chart = VizzuChart(key="vizzu", height=380)
chart.animate(data)
if "story" not in st.session_state:
    st.session_state.story = Story(data)
    st.session_state.story.set_feature("tooltip", True)
chart.feature("tooltip", True)

split = st.session_state.get("split", False)
chart_type = st.session_state.get("chart_type", "Column")

defaultFormats = ["Cassette", "CD", "Download", "Vinyl"]
allFormats = defaultFormats + ["DVD", "Other", "Streaming", "Tape"]

# -- subheading style setting --
st.write("""
<style>
.small-font {
    font-size:14px !important;
    margin-bottom:0.5rem !important;
}
</style>
""", unsafe_allow_html=True)

# -- define controllers on the Sidebar --
with st.sidebar:
    col1, col2 = st.columns(2)

    compare_by = col1.radio("Compare by", ["Revenue", "Volume"])
    stack_by = col2.radio("Stack by", ["Year", "Format"])

    st.write('<p class="small-font">Additional options</p>',
             unsafe_allow_html=True)

# -- select time range --
year1, year2 = st.select_slider(
    "Time range",
    options=map(str, np.arange(1973, 2019)),
    value=('1980', '2010')
)

filter_year = f"record['Year'] >= {year1} && record['Year'] <= {year2}"

# -- choose continuous value --
with st.sidebar:
    adjust = st.checkbox("Adjust for inflation",
                         disabled=compare_by != "Revenue")

# -- set dynamic title --
titleMeasure = "Revenues" if compare_by == "Revenue" else "Sales Volumes"

title = f"Music {titleMeasure} by {stack_by} " + \
        (f"in {year1}" if year1 == year2 else f"between {year1} and {year2}")

filter_metric = "record['Metric'] == " + (
    "'Units'" if compare_by != "Revenue" else 
    "'Value (Adjusted)'" if adjust else "'Value'")

# -- choose grouping category --
measure = "Revenue[$]" if compare_by == "Revenue" else "Units"

color = "Format"

if stack_by == "Year":
    x = "Year"
    y = [measure, "Format"]
    label = None
else:
    y = "Format"
    x = measure
    label = measure

with st.sidebar:
    sort = st.checkbox("Sort by value", disabled=stack_by == "Year")

# -- select format --
items: List[str] = st.multiselect(
    "Format", allFormats, defaultFormats, key="multiselect")

filter_format = "(" + \
    " || ".join([f"record['Format'] == '{item}'" for item in items]) + ")"

# -- concat filters --
filter = " && ".join([filter_metric, filter_year, filter_format])

# -- set config --
config = {
    "title": title,
    "y": y,
    "x": x,
    "color": color,
    "label": label
}

config["sort"] = "byValue" if sort and stack_by != "Year" else "none"

if chart_type == "Stream" and stack_by != "Format":
    config["geometry"] = "area"
    config["align"] = "center"
else:
    config["geometry"] = "rectangle"
    config["align"] = "none"

config["split"] = split and stack_by != "Format"

# -- define controllers on the Sidebar --
def show_default():
    st.session_state.multiselect = defaultFormats
    return

def show_all():
    st.session_state.multiselect = allFormats
    return

with st.sidebar:
    st.write('<p class="small-font">Format multiselect</p>',
             unsafe_allow_html=True)
    col5, col6 = st.columns(2)
    col6.button("All Formats", on_click=show_all)
    col5.button("Selected Formats", on_click=show_default)

# -- style settings --
angle = "0.0"
xAxisLabelColor = "#999999FF"
yAxisLabelColor = "#999999FF"
plotPaddingLeft = "7.5em"

if stack_by == "Year":
    angle = "-1.1"
else:
    xAxisLabelColor = "#00000000"
    plotPaddingLeft = "9em"

if split == True and stack_by != "Format":
    yAxisLabelColor = "#00000000"

style = Style({
    "plot": {
        "xAxis": {
            "label": {
                "angle": angle,
                "color": xAxisLabelColor,
                "fontSize": "0.9em",
                'numberFormat': 'prefixed',
                'numberScale': 'shortScaleSymbolUS'
            }
        },
        "yAxis": {
            "label": {
                "color": yAxisLabelColor,
                'numberFormat': 'prefixed',
                'numberScale': 'shortScaleSymbolUS'
            }
        },
        "marker": {
            "colorPalette": "#b74c20FF #c47f58FF #1c9761FF #ea4549FF #875792FF #3562b6FF #ee7c34FF #efae3aFF",
            'label': {
                'numberFormat': 'prefixed',
                'maxFractionDigits': '1',
                'numberScale': 'shortScaleSymbolUS'
            }
        },
        "paddingLeft": plotPaddingLeft
    },
    "legend": {
        "paddingRight": "-4em"
    },
    "logo": {
        "paddingBottom": "1.5em"
    }
})

# -- display chart --
chart.animate(Data.filter(filter), Config(config), style, delay="0.1")
st.session_state.story.add_slide(Slide(Step(Data.filter(filter), Config(config), style)))
output = chart.show()

# -- set controllers under the chart --
col3, col4 = st.columns(2)

col4.write('<p class="small-font">ㅤㅤ‎</p>', unsafe_allow_html=True)

split = col4.checkbox("Split values", key="split", disabled=stack_by != "Year")
chart_type = col3.radio("Chart type", [
                        "Column", "Stream"], key="chart_type", horizontal=True, disabled=stack_by != "Year")

st.download_button(label="Download Story", data=st.session_state.story.to_html(), file_name="story.html", mime="text/html")