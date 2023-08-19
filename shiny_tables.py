from shiny import ui
from numpy import nan_to_num
import pandas as pd


def _clean_header_names(x):
    if isinstance(x, str):
        return x.replace('_', ' ').title()
    return x


def process_header_class(col_name, cell_style_dict, active=False):
    if not active:
        return
    style = ""
    if cell_style_entry := cell_style_dict.get(col_name):
        if callable(cell_style_entry):
            if theStyle := cell_style_entry(col_name):
                assert isinstance(
                    theStyle, dict), "cell_style Callable must return a dict"
                style = theStyle
    if the_class := style.get('className'):
        return the_class
    return None


def enhanced_from_dataframe(
    df,
    columns=None,
    link_column_suffix='_HREF',
    cell_style_dict=None,
    float_format='.2f',
    index=False,
    index_label=None,
    date_format="%Y-%m-%d",
    header_callable=None,
    link_target=None,
    button_columns=None,
    markdown_columns=None,
    process_header_classes=False,  ## if true the cell style dict callable  will apply to header
    **table_kwargs):
    """make a dash table from a pandas dataframe but add hyperlinks based on matching column names. Conditionally style a column or columns
    
    cell_style_dict: dict of {column_name: {condition: style_dict}}
    
    condition can be astring or a function that returns a boolean

    if condition is a string, it must match the value of the column exactly. 
    
    """
    if df.empty:
        return ui.tags.div()
    if index:
        df = df.reset_index()
        if index_label is not None:
            df = df.rename(columns={"index": index_label})

    if date_format is not None:
        for c in df.select_dtypes(["datetime"]).columns:
            df[c] = pd.to_datetime(df[c])

    if columns is not None:
        # needed in case columns keyword would otherwise remove  out the link column
        column_order_dict = {key: val for val, key in enumerate(columns)}
        columns = sorted(set(
            list(columns) +
            [f"{col + link_column_suffix}"
             for col in df.columns]).intersection(set(df.columns)),
                         key=lambda x: column_order_dict.get(x, float('inf')))
    else:
        columns = df.columns
    data_dict = df[columns].to_dict(orient='records')
    if cell_style_dict is None:
        cell_style_dict = {}

    col_names = list(data_dict[0].keys())
    if header_callable is None:
        header_column_cells = [
            ui.tags.th(_clean_header_names(x),
                       className=process_header_class(
                           x,
                           cell_style_dict=cell_style_dict,
                           active=process_header_classes)) for x in col_names
            if not str(x).endswith(link_column_suffix)
        ]
    else:
        assert callable(header_callable), "header_callable must be callable"
        header_column_cells = [
            ui.tags.th(header_callable(_clean_header_names(x)),
                       className=process_header_class(
                           x, cell_style_dict, active=process_header_classes))
            for x in col_names if not str(x).endswith(link_column_suffix)
        ]
    table_header = [ui.tags.thead(ui.tags.tr(header_column_cells))]
    table_body = [
        ui.tags.tbody([
            _make_row(x,
                      col_names,
                      link_column_suffix,
                      cell_style_dict=cell_style_dict,
                      float_format=float_format,
                      date_format=date_format,
                      link_target=link_target,
                      button_columns=button_columns,
                      markdown_columns=markdown_columns) for x in data_dict
        ])
    ]
    return ui.tags.table(table_header + table_body, {
        'class': 'table table-striped',
        'style': 'width: 75%'
    })


def _make_row(data_dict_entry,
              col_names,
              link_column_suffix,
              cell_style_dict=None,
              float_format='.2f',
              date_format=None,
              link_target=None,
              button_columns=None,
              markdown_columns=None):
    if button_columns is None:
        button_columns = []
    if markdown_columns is None:
        markdown_columns = []

    if link_target is None:
        link_target = ''
    if cell_style_dict is None:
        cell_style_dict = {}

    def process_table_cell(
        col_name,
        link_names,
    ):
        """Add links to tables in the right way and handle nan strings."""
        shiny_style_class_dict = {}
        if cell_style_entry := cell_style_dict.get(col_name):
            if isinstance(cell_style_entry, list):
                for item in cell_style_entry:
                    if data_dict_entry[col_name] in item[0]:
                        shiny_style_class_dict = item[1]

            elif callable(cell_style_entry):
                if theStyle := cell_style_entry(data_dict_entry[col_name]):
                    assert isinstance(
                        theStyle,
                        dict), "cell_style Callable must return a dictionary"
                    shiny_style_class_dict = theStyle
            else:
                shiny_style_class_dict = {}
        print(col_name)
        print(shiny_style_class_dict)
        if (thehref := f"{col_name}{link_column_suffix}") in link_names:

            if data_dict_entry[thehref].startswith("http"):
                return ui.tags.td(
                    ui.tags.a(
                        str(data_dict_entry[col_name]),
                        target=link_target,
                        href=str(data_dict_entry[thehref], ),
                    ), shiny_style_class_dict)
            return ui.tags.td(
                ui.tags.link(
                    str(data_dict_entry[col_name]),
                    href=str(data_dict_entry[thehref], shiny_style_class_dict),
                ))
        # elif col_name in button_columns:
        #     return ui.tags.td(
        #         ui.input_action_button(
        #             data_dict_entry[col_name].title(),
        #             id=f'{col_name}-button-{data_dict_entry[col_name]}'))
        elif col_name in markdown_columns:
            return ui.tags.td(ui.markdown(data_dict_entry[col_name]), )
        elif isinstance(data_dict_entry[col_name], float):
            return ui.tags.td(
                f"{nan_to_num(data_dict_entry[col_name]):{float_format}}",
                shiny_style_class_dict)
        elif isinstance(data_dict_entry[col_name], int):
            return ui.tags.td(f"{data_dict_entry[col_name]:,}")
        elif date_format and isinstance(data_dict_entry[col_name],
                                        pd.Timestamp):

            return ui.tags.td(data_dict_entry[col_name].strftime(date_format),
                              shiny_style_class_dict)
        return ui.tags.td(str(data_dict_entry[col_name]), )

    link_names = [x for x in col_names if str(x).endswith(link_column_suffix)]
    return ui.tags.tr([
        process_table_cell(x, link_names) for x in col_names
        if not str(x).endswith(link_column_suffix)
    ])
