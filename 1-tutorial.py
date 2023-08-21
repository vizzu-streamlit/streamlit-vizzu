import pandas as pd
import streamlit as st
from streamlit_vizzu import Config, Data, VizzuChart

# Create a VizzuChart object with the default height and width
chart = VizzuChart()

# Generate some data and add it to the chart
df = pd.DataFrame({"cat": ["x", "y", "z"], "val": [1, 2, 3]})
data = Data()
data.add_data_frame(df)
chart.animate(data)

st.subheader(
    "Visit [intro-to-vizzu-in.streamlit.app](https://intro-to-vizzu-in.streamlit.app/) "
    "to follow along"
)

# Add some configuration to tell Vizzu how to display the data
chart.animate(Config({"x": "cat", "y": "val", "title": "Look at my plot!"}))

if st.checkbox("Swap"):
    chart.animate(Config({"x": "val", "y": "cat", "title": "Swapped!"}))

# Show the chart in the app!
output = chart.show()

if output is not None and "marker" in output:
    st.write("value of clicked bar:", output["marker"]["values"]["val"])

st.caption("Data shown on the chart")
st.dataframe(df)

st.write(
    "Check the [source code](https://github.com/vizzu-streamlit/streamlit-vizzu) "
    "of the bidirectional component that makes this possible, created by "
    "[blackary](https://github.com/blackary)"
)
