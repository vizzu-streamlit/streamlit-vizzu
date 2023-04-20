import pandas as pd
import streamlit as st

from streamlit_vizzu import Config, Data, VizzuChart

st.header('Thanks for using the app! :heart_eyes:') 
col1, col2 = st.columns(2)
with col1:
	st.markdown('If you want to learn more about how it works, check out this [blog post](https://blog.streamlit.io/create-an-animated-data-story-with-ipyvizzu-and-streamlit/) on creating animated data stories with ipyvizzu and Streamlit. :chart_with_upwards_trend::film_frames::balloon:')
	st.markdown('You can find the code for the app on this [GitHub repo](https://github.com/vizzu-streamlit/world-population-story)')
	st.markdown('Visit our [homepage](https://vizzuhq.com)] to learn more about our open-source charting and data storytelling tools.')
with col2:
	st.markdown('![homepage [homepage](https://vizzuhq.com)](https://github.com/vizzuhq/vizzu-lib-doc/raw/main/docs/readme/infinite-60.gif)')			

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
data = chart.show()

if data is not None and "marker" in data:
    st.write("value of clicked bar:", data["marker"]["values"]["b"])
