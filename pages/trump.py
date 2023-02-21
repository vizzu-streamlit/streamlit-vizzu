import pandas as pd
import streamlit as st
from ipyvizzu.animation import Config, Data
from streamlit_vizzu import VizzuChart as Chart


@st.cache_data
def get_data() -> pd.DataFrame:
    return pd.read_csv(
        "https://raw.githubusercontent.com/vizzuhq/vizzu-workshops/main/2022-11-11-PyData-NYC/data/trump_2020_05.csv"
    )


data = Data()

data.add_data_frame(get_data())

vchart = Chart(height=360, return_clicks=False)

vchart.animate(data)

if "slide_num" not in st.session_state:
    try:
        st.session_state["slide_num"] = int(
            st.experimental_get_query_params()["slide_num"][0]
        )
    except (KeyError, ValueError, IndexError):
        st.session_state["slide_num"] = 0

CHANNELS = {
    "channels": {
        "y": {
            "set": ["tweets"],
        },
        "x": {"set": ["Period", "year", "month"]},
        "color": "Period",
    }
}


previous_slide = st.button(
    "Previous slide", disabled=st.session_state["slide_num"] == 0
)
if previous_slide:
    st.session_state["slide_num"] -= 1

next_slide = st.button("Next slide", disabled=st.session_state["slide_num"] >= 9)
if next_slide:
    st.session_state["slide_num"] += 1

if st.session_state["slide_num"] == 0:
    vchart.animate(
        Data.filter("record.Firsttweet === 'Igen' && record.Dummy === 'Nem'"),
        Config(
            {
                **CHANNELS,  # type: ignore
                "title": "Trump started tweeting in May '09",
            }
        ),
    )
elif st.session_state["slide_num"] == 1:
    vchart.animate(
        Data.filter("record.Period === 'New to Twitter' && record.Dummy === 'Nem'"),
        Config(
            {
                "title": "In the first two years he wasn't very active",
                **CHANNELS,  # type: ignore
            }
        ),
    )
elif st.session_state["slide_num"] == 2:
    vchart.animate(
        Data.filter(
            "(record.Period === 'New to Twitter' || record.Period === 'Businessman') "
            "&& record.Dummy === 'Nem'"
        ),
        Config(
            {
                "title": "Then he got hooked on",
                **CHANNELS,  # type: ignore
            }
        ),
    )

elif st.session_state["slide_num"] == 3:
    vchart.animate(
        Data.filter(
            "(record.Period === 'New to Twitter' || record.Period === 'Businessman' "
            "|| record.Period === 'Nominee') && record.Dummy === 'Nem'"
        ),
        Config(
            {
                "title": "Interesting trend after becoming a presidential nominee",
                **CHANNELS,  # type: ignore
            }
        ),
    )

elif st.session_state["slide_num"] == 4:
    vchart.animate(
        Data.filter("record.Dummy === 'Nem'"),
        Config(
            {
                "title": "And after he became President",
                **CHANNELS,  # type: ignore
            }
        ),
    )

elif st.session_state["slide_num"] == 5:
    vchart.animate(
        Config(
            {
                "geometry": "area",
                "align": "center",
                **CHANNELS,  # type: ignore
            }
        ),
    )

elif st.session_state["slide_num"] == 6:
    vchart.animate(
        Config(
            {
                "title": "All of Trump's tweets until May 2020",
                **CHANNELS,  # type: ignore
            }
        ),
    )

elif st.session_state["slide_num"] == 7:
    vchart.animate(
        Config(
            {
                "y": "retweetcount",
                "title": "And the number of times these were retweeted",
            }
        ),
    )

elif st.session_state["slide_num"] == 8:
    vchart.animate(
        Config(
            {
                "y": "tweets",
                "title": "Let's focus on the number of tweets for now",
            }
        ),
    )
    st.write("Sorry, only did 8 slides for now")

vchart.show()
