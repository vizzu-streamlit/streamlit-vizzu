import altair as alt
import pandas as pd
import streamlit as st
from streamlit_extras.altex import _chart

from streamlit_vizzu import Config, Data, VizzuChart

st.set_page_config(layout="centered", page_title="Data Editor", page_icon="🧮")

st.title("📊 Data to Chart")
st.caption("This is a demo of the `st.data_editor`.")

"Let viewers edit your data and see how that impacts the rest of the app!"


@st.cache_data
def get_data() -> pd.DataFrame:
    df = pd.DataFrame(
        {
            "age": [12, 32, 45, 90, 89],
            "gender": ["male", "male", "other", "female", "male"],
            "active": [False, True, True, True, False],
            "count": [1, 1, 1, 1, 1],
        },
    )

    df.age = df.age.astype("uint64")
    return df


# Create a VizzuChart object with the default height and width
chart = VizzuChart(
    default_duration=0.3,
)

empty_data = pd.DataFrame(
    {
        "age": [],
        # "gender": [],
        "active": [],
        "count": [],
    }
)
empty_data.age = empty_data.age.astype("int64")
empty_data_object = Data()
empty_data_object.add_data_frame(empty_data)
chart.animate(empty_data_object)


@st.cache_data
def get_age_hist(df: pd.DataFrame) -> alt.Chart:
    return _chart(
        mark_function="bar",
        data=pd.cut(
            df.age,
            (0, 18, 30, 60, 100),
            labels=["0 - 18", "18 - 30", "30 - 60", "60 - 100"],
        )
        .value_counts()
        .sort_index()
        .reset_index(),
        x=alt.X("index:N", title="Age", sort="x"),
        y=alt.Y("age:Q", title="Count"),
    )


@st.cache_data
def get_gender_hist(df: pd.DataFrame) -> alt.Chart:
    return _chart(
        mark_function="bar",
        data=df.gender.value_counts().sort_index().reset_index(),
        x=alt.X("index:N", title="Gender", sort="x"),
        y=alt.Y("gender:Q", title=""),
    )


@st.cache_data
def get_active_hist(df: pd.DataFrame) -> alt.Chart:
    return _chart(
        mark_function="bar",
        data=df.active.value_counts().sort_index().reset_index(),
        x=alt.X("index:N", title="Active", sort="x"),
        y=alt.Y("active:Q", title=""),
    )


with st.echo():
    df = get_data()
    edited_df = st.data_editor(
        df,
        use_container_width=True,
        num_rows="dynamic",
    )

st.caption("Modify cells above 👆 or even ➕ add rows, and check out the impacts below 👇")

data = Data()
data.add_data_frame(edited_df)
chart.animate(data, Config({"x": "gender", "y": "count", "title": "Blah"}))
chart.animate(
    Data.filter("record['active'] == true"),
    Config({"x": "gender", "y": "count", "title": "Blah"}),
)

chart.show()