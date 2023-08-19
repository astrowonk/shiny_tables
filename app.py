from shiny import App, render, ui
import pandas as pd
from shiny_tables import enhanced_from_dataframe
import datetime

the_list = [
    "Apple", "Google", "Yahoo", "Facebook", "Microsoft", "Amazon", "IBM",
    "Intel", "Oracle"
]
start_date = datetime.datetime(2018, 1, 1)
date_list = pd.date_range(start_date, periods=len(the_list)).tolist()

df = pd.DataFrame([{
    'Company':
    x,
    "Company_HREF":
    f"https://{x.lower()}.com",
    "Value": (n - 4) / 13,
    "Value2": (n**4) / 13,
    "Date":
    date_list[n],
    "markdown_example":
    f"""Everything in **here** is plain text in _Markdown_, created with an fstring for Company **{x}** """
} for n, x in enumerate(the_list)])


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
    },  ## these needed because the callable gets applied on the string header. 
    ## maybe the header should have its own callable tha controls class
    'Date':
    lambda x: {
        'class': 'table-danger'
    } if x.weekday() in [4, 6] else {},
    'Value':
    color_positive
}

app_ui = ui.page_fluid(
    ui.output_ui("result"),
    # Legend
    ui.panel_conditional(
        "input.highlight",
        ui.panel_absolute(
            ui.span("minimum", style="background-color: silver;"),
            ui.span("maximum", style="background-color: yellow;"),
            top="6px",
            right="6px",
            class_="p-1 bg-light border",
        ),
    ),
    class_="p-3",
)


def server(input, output, session):

    @output
    @render.ui
    def result():
        return enhanced_from_dataframe(df,
                                       markdown_columns=['markdown_example'],
                                       cell_style_dict=cell_style_dict)


app = App(app_ui, server)
