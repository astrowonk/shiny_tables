
### Bootstrap Tables from a DataFrame

This function will automatically generate `html.A` wrappers around a column from a __matched column in the same dataframe__.  The hyperlink column must match the column_name + a specific suffix. In the example to the right, the (hidden) link column is `Company_HREF`, using the default suffix.

Conditional Formatting criteria can either be a list of tuples `(match_list,style_dict)` or a `callable` that returns the style dict if the condition is met. This allows for more complex condition formatting.

The code below generates the conditional formatting you see. You can also add a specific bootstrap class by putting a `className` key in the "style" dictionary.

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
        "style": 'background-color: rgb(170, 111, 241)'
    } if x > 10 else {
    },  ## these needed because the callable gets applied on the string header. 
    ## maybe the header should have its own callable tha controls class
    'Date':
    lambda x: {
        'class': 'table-danger'
    } if x.weekday() in [4, 6] else {},
    'Value':
    color_positive
}
```
