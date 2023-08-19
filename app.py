from shiny import App, render, ui
import pandas as pd
from shiny_tables import enhanced_from_dataframe
import datetime
import shinyswatch

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
    f"""**Everything** in this cell is plain text in _Markdown_, created with an fstring for Company **{x}** """
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
        'class': 'table-info'
    } if x.weekday() in [4, 6] else {},
    'Value':
    color_positive
}

with open("about.md", "r") as myfile:
    about_text = myfile.read()

app_ui = ui.page_bootstrap(
    shinyswatch.theme.yeti(),
    ui.head_content(
        #     ui.tags.link({
        #         "href":
        #         "https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css",
        #         "rel": "stylesheet"
        #     }),
        ui.tags.script({
            'src':
            "https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.8.0/build/highlight.min.js"
        }),
        ui.tags.link({
            "href":
            "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/github.min.css",
            "rel": "stylesheet"
        }),
        ui.tags.script('hljs.highlightAll();')),
    ui.panel_title("Demo Bootstrap tables for Shiny Python."),
    ui.row(
        ui.column(6, ui.markdown(about_text)),
        ui.column(6, ui.output_ui("result")),
    ),
    {'style': "margin: 10px auto; width: 85%"})


def server(input, output, session):

    @output
    @render.ui
    def result():
        return enhanced_from_dataframe(
            df,
            markdown_columns=['markdown_example'],
            cell_style_dict=cell_style_dict,
            columns=['Company', 'Date', 'Value', 'Value2', 'markdown_example'])


app = App(app_ui, server)
