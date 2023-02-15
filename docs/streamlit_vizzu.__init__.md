<!-- markdownlint-disable -->

<a href="../src/streamlit_vizzu/__init__.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `streamlit_vizzu.__init__`






---

<a href="../src/streamlit_vizzu/__init__.py#L20"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `VizzuChart`




<a href="../src/streamlit_vizzu/__init__.py#L21"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    width: 'int' = 700,
    height: 'int' = 480,
    key: 'str' = 'vizzu',
    return_clicks: 'bool' = True,
    rerun_on_click: 'bool' = False,
    default_duration: 'float | None' = None,
    **kwargs
)
```

Create a VizzuChart object for use in a streamlit app 

width: specify width of chart in pixels height: specify height of chart in pixels key: specify unique key for chart, defaults to `vizzu` return_clicks: specify whether or not the chart should return values             when clicked rerun_on_click: if True, and return_clicks is True, will call             st.experimental_rerun() whenever your chart is clicked default_duration: specify the default duration that will be applied to all             animations, in seconds 


---

#### <kbd>property</kbd> scroll_into_view

A property for turning on/off scroll into view. 



---

<a href="../src/streamlit_vizzu/__init__.py#L133"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `animate`

```python
animate(*animations: 'Any', **options: 'Any')
```

Pass any number of Animation objects (e.g. Data, Config, or Style objects), and any options that should be applied to them. 

---

<a href="../src/streamlit_vizzu/__init__.py#L90"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get`

```python
get(dotted_key: 'str', default: 'Any' = None) → Any
```

Pass a dot-separated key to access a specific value from the latest click (e.g. "marker.categories.a"). If there hasn't been a click, or that path isn't found, return the default value. 

---

<a href="../src/streamlit_vizzu/__init__.py#L63"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `show`

```python
show()
```

Render your chart within your streamlit app. Note that any animations applied after your chart is shown will not affect the chart. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
