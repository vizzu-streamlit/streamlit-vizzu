import pandas as pd
import streamlit as st
from ipyvizzu.animation import Config, Data, Style

from streamlit_vizzu import VizzuChart

data_frame = pd.read_csv(
    "data/music2.csv", dtype={"Year": str}
)

data = Data()
data.add_data_frame(data_frame)

chart = VizzuChart(key="vizzu", height=380)
chart.animate(data)
chart.feature("tooltip", True)

split = st.session_state.get("split", False)
chart_type = st.session_state.get("chart_type", "Column")

def set_default():
    st.session_state.multiselect = ["Cassette", "CD", "Download", "Vinyl"]
    return

def show_all():
    st.session_state.multiselect = ["Cassette", "CD", "Download", "DVD", "Other", "Streaming", "Tape", "Vinyl"]
    return

# -- subheading style setting --
st.write("""
<style>
.small-font {
    font-size:14px !important;
    margin-bottom:0.5rem !important;
}
</style>
""", unsafe_allow_html=True)

# -- set default variables --
x = ["Year"]
y = ["Revenue[$]"]
color = ["Format"]
label = None

angle = "0.0"
xAxisLabelColor = "#999999FF"
yAxisLabelColor = "#999999FF"
plotPaddingLeft = "7.5em"
xAxisFontSize = "0.9em"

# -- define controllers on the Sidebar --
with st.sidebar:
    col1, col2 = st.columns(2)

    compare_by = col1.radio("Compare by", [ "Revenue", "Volume"])
    stack_by = col2.radio("Stack by", ["Year", "Format"])

    st.write('<p class="small-font">Additional options</p>', unsafe_allow_html=True)

# -- select time range --
year1, year2 = ('1980','1982')

year1, year2 = st.select_slider(
    "Time range",
    options=['','1973','1974','1975','1976','1977','1978','1979',
    '1980','1981','1982','1983','1984','1985','1986','1987','1988','1989',
    '1990','1991','1992','1993','1994','1995','1996','1997','1998','1999',
    '2000','2001','2002','2003','2004','2005','2006','2007','2008','2009',
    '2010','2011','2012','2013','2014','2015','2016','2017','2018','2019',''], 
    value=('1980','2010')
)

years = ['','1973','1974','1975','1976','1977','1978','1979',
'1980','1981','1982','1983','1984','1985','1986','1987','1988','1989',
'1990','1991','1992','1993','1994','1995','1996','1997','1998','1999',
'2000','2001','2002','2003','2004','2005','2006','2007','2008','2009',
'2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','']

for item in years.copy():
    if (item < year1 and year1 != "") or (item > year2 and year2 != ""):
        years.remove(item)

filter_year = "(" + " || ".join([f"record['Year'] == '{item}'" for item in years]) + ")"

# -- choose continuous value --
if compare_by == "Revenue":

    with st.sidebar:
        adjust = st.checkbox("Adjust for inflation")

    # -- set dynamic title --    
    if year1 == year2 != "":
        title = f"Music Revenues by {stack_by} in {year1}"
    elif year1 != "" and year2 == "":
        title = f"Music Revenues by {stack_by} between {year1} and 2019"
    elif year1 == "" and year2 != "":
        title = f"Music Revenues by {stack_by} between 1973 and {year2}"
    elif year1 != "" and year2 != "":
        title = f"Music Revenues by {stack_by} between {year1} and {year2}"
    else:
        title = f"Music Revenues by {stack_by} between 1973 and 2019"

    # -- adjust value for inflation --
    if adjust:
        filter_metric = "record['Metric'] == 'Value (Adjusted)'"
    else:
        filter_metric = "record['Metric'] == 'Value'" 

    # -- choose grouping category --
    if stack_by == "Year":
        x = "Year"
        y = ["Revenue[$]", "Format"]
        color = "Format"
        angle = "-1.1"

        with st.sidebar:
            sort = st.checkbox("Sort by value", disabled = True)   

    else:
        y = "Format"
        x = "Revenue[$]"
        label = "Revenue[$]"
        xAxisLabelColor = "#00000000"
        plotPaddingLeft = "9em" 

        with st.sidebar:
            sort = st.checkbox("Sort by value")   

else: 

    filter_metric = "record['Metric'] == 'Units'"

    with st.sidebar:
        adjust = st.checkbox("Adjust for inflation", disabled = True)

    if year1 == year2 != "":
        title = f"Music Sales Volumes by {stack_by} in {year1}"
    elif year1 != "" and year2 == "":
        title = f"Music Sales Volumes by {stack_by} between {year1} and 2019"
    elif year1 == "" and year2 != "":
        title = f"Music Sales Volumes by {stack_by} between 1973 and {year2}"
    elif year1 != "" and year2 != "":
        title = f"Music Sales Volumes by {stack_by} between {year1} and {year2}"
    else:
        title = f"Music Sales Volumes by {stack_by} between 1973 and 2019"

    if stack_by == "Year":
        x = "Year"
        y = ["Units", "Format"]
        color = "Format"
        angle = "-1.1"

        with st.sidebar:
            sort = st.checkbox("Sort by value", disabled = True)
            
    else:
        y = "Format"
        x = "Units"
        label = "Units"
        xAxisLabelColor = "#00000000"
        plotPaddingLeft = "9em" 

        with st.sidebar:
            sort = st.checkbox("Sort by value")  

# -- select format --
items: list[str] = st.multiselect(  
    "Format",
    ["Cassette", "CD", "Download", "DVD", "Other", "Streaming", "Tape", "Vinyl"],
    ["Cassette", "CD", "Download", "Vinyl"], key="multiselect"
)

filter_format = "(" + " || ".join([f"record['Format'] == '{item}'" for item in items]) + ")"

# -- concat filters --
filter = " && ".join([filter_metric,filter_year,filter_format])

# -- set config --
config = {
    "title": title,
    "y": y,
    "x": x,
    "color": color,
    "label": label
}

if sort and stack_by != "Year":
    config["sort"] = "byValue"
else:
    config["sort"] = "none"

if chart_type == "Stream" and stack_by != "Format":
    config["geometry"] = "area"
    config["align"] = "center"
else:
    config["geometry"] = "rectangle"
    config["align"] = "none"

if split == True and stack_by != "Format":
    config["split"] = True
else:
    config["split"] = False

# -- define controllers on the Sidebar --
with st.sidebar:
    st.write('<p class="small-font">Format multiselect</p>', unsafe_allow_html=True)
    col5, col6 = st.columns(2)

    col6.button("All Formats", on_click=show_all)
    col5.button("Selected Formats", on_click=set_default)


# -- style settings --

if split == True and stack_by != "Format":
    yAxisLabelColor = "#00000000"

style = Style({
    "plot": {
        "xAxis": {
            "label": {
                "angle": angle,
                "color": xAxisLabelColor,
                "fontSize": xAxisFontSize,
				'numberFormat' : 'prefixed', 
				'numberScale':'shortScaleSymbolUS'
            }
        },
        "yAxis": {
            "label": {
                "color": yAxisLabelColor,
				'numberFormat' : 'prefixed', 
				'numberScale':'shortScaleSymbolUS'
            }
        },
		"marker": { 
			"colorPalette": "#b74c20FF #c47f58FF #1c9761FF #ea4549FF #875792FF #3562b6FF #ee7c34FF #efae3aFF",
			'label' :{ 
				'numberFormat' : 'prefixed',
				'maxFractionDigits' : '1',
				'numberScale':'shortScaleSymbolUS'
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
output = chart.show()

# -- set controllers under the chart --
col3, col4 = st.columns(2)

col4.write('<p class="small-font">ㅤㅤ‎</p>', unsafe_allow_html=True)

if stack_by == "Year": 
    split = col4.checkbox("Split values", key="split")
    chart_type = col3.radio("Chart type", ["Column", "Stream"], key="chart_type", horizontal=True) 
else:
    split = col4.checkbox("Split values", key="split", disabled=True)
    chart_type = col3.radio("Chart type", ["Column", "Stream"], key="chart_type", disabled=True, horizontal=True)


