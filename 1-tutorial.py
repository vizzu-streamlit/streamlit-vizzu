import pandas as pd
import streamlit as st
from streamlit_vizzu import Config, Data, VizzuChart

# Create a VizzuChart object with the default height and width
chart = VizzuChart()

# Generate some data and add it to the chart
df = pd.DataFrame({"a": ["x", "y", "z"], "b": [1, 2, 3]})
data = Data()
data.add_data_frame(df)
chart.animate(data)

# Add some configuration to tell Vizzu how to display the data
chart.animate(Config({"x": "a", "y": "b", "title": "Look at my plot!"}))

if st.checkbox("Swap"):
    chart.animate(Config({"y": "a", "x": "b", "title": "Swapped!"}))

# Show the chart in the app!
output = chart.show()

if output is not None and "marker" in output:
    st.write("value of clicked bar:", output["marker"]["values"]["b"])


st.write(
    "Check the [source code](https://github.com/vizzu-streamlit/streamlit-vizzu) "
    "of the bidirectional component that makes this possible, created by "
    "[blackary](https://github.com/blackary)"
)
