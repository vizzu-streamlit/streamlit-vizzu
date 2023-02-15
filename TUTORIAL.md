# Streamlit-Vizzu Tutorial

## Installation

To get started with Streamlit-Vizzu, first you need to install the package

```sh
pip install streamlit-vizzu
```

## Create your first chart

To create a streamlit-vizzu chart, you will need, at minimum, some data to
display, and some configuration to tell Vizzu how to display it.

Create a file called `streamlit_app.py` with the following content

```python
import pandas as pd
from ipyvizzu.animation import Config, Data

from streamlit_vizzu import VizzuChart

# Create a VizzuChart object with the default height and width
chart = VizzuChart()

# Generate some data and add it to the chart
df = pd.DataFrame({"a": ["x", "y", "z"], "b": [1, 2, 3]})
data = Data()
data.add_data_frame(df)
chart.animate(data)

# Add some configuration to tell Vizzu how to display the data
chart.animate(Config({"x": "a", "y": "b", "title": "Look at my plot!"}))

# Show the chart in the app!
chart.show()
```
