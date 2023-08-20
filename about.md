
### Bootstrap Tables from a DataFrame

## Features

This `enhanced_from_dataframe` function creates bootstrap tables with some automatic features like links and conditional formatting.

* **Automatic Links** It will automatically generate `ui.tags.A` wrappers around a column from a __matched column in the same dataframe__.  The hyperlink column must match the column_name + a specific suffix. In the example to the right, the (hidden) link column is `Company_HREF`, using the default suffix.
* **Conditional Formatting** Criteria can either be a list of tuples `(match_list,style_dict)` or a `callable` that returns the style dict if the condition is met. This allows for more complex condition formatting.
* **Any Callable can wrap a cell** Pass a callable to the function to customize the content of any column. Turn it into a button, link, wrap it in any UII elements you can create in Shiny.

## How to use
This is invoked with render.ui and outputting to a ui output:

```python
        
def server(input, output, session):

    @output
    @render.ui
    def result():
        return enhanced_from_dataframe(
            df,
            markdown_columns=['markdown_example'],
            cell_style_dict=cell_style_dict,
            columns=[
                'Company', 'Company2', 'Date', 'Value', 'Value2',
                'markdown_example'
            ],
            column_callable_dict={'Company2': wrap_company},
            )



```


The code below generates the conditional formatting you see. You can also add a specific bootstrap class by putting a `class` key in the "style" dictionary.

```python

def color_positive(val):
    if val > 0:
        return {'class': 'table-success'}
    elif val < 0:
        return {'class': "table-danger"}


cell_style_dict = {
    'Company': [
        (['Yahoo', 'Apple'], {
            "style": 'font-weight: bold'
        }),
        (['Oracle'], {
            'class': 'table-danger'
        }),
    ],
    'Value2':
    lambda x: {
        "style": 'background-color: #7FFFD4'
    } if x > 10 else {
    }
    'Date':
    lambda x: {
        'class': 'table-info'
    } if x.weekday() in [4, 6] else {},
    'Value':
    color_positive
}
```

This code has the callable wrapper for the Company2 column:

```python

def wrap_company(row, col_name):
    return experimental.ui.tooltip(
        ui.tags.button(row[col_name], ),
        f"This is a tool tip for {row[col_name]} that shows the link {row['Company_HREF']}"
    )



```