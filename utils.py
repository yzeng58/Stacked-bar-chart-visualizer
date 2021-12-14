import numpy as np
import base64, datetime, io, random
import pandas as pd
import dash_html_components as html


def parse_contents(contents, filename):
    _, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        assert(filename.split('.')[-1] == 'csv')
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
    except Exception as e:
        return html.Div([
            'Only .csv file is supported.'
        ])
    return df

def bar_num(df, width, height, x, y):
    len_x = len(df[x])
    num = width // 20 if width / len_x < 20 else len_x
    return num

def sample_prob(num, df, x, y):
    random.seed(123)
    max_bar, min_bar = df.y_total.idxmax(), df.y_total.idxmin()
    idxs = df.index.tolist()
    idxs.remove(max_bar)
    idxs.remove(min_bar)
    idxs = random.sample(idxs, num-2) + [max_bar, min_bar]
    return sorted(idxs)

def process_df(df, width, height, x, y, sort_opt):
    df = clean_df(df, y)
    bar_width = 0.7

    # sort
    len_x = len(df[x])
    df['y_total'] = df[y].apply(func = sum, axis = 1)
    opt = True if sort_opt == 'a' else False
    df = df.sort_values(by = 'y_total', ascending = opt)
    df[x] = df[x].apply(func = lambda x: str(x)[:height//25]).reset_index(drop = True)

    num = bar_num(df, width, height, x, y)
    if num < len_x: # need subset
        if sort_opt == 'n': # subsampling
            selected_idxs = sample_prob(num, df, x, y)
            df = df.loc[selected_idxs]
        else: # ascending or descending
            df = df[:num]
        bar_width = 1
    return df.reset_index(drop = True), bar_width

def clean_df(df,ys):
    '''Check the validity of the input dataset.
    Args:
        df: the input data set, should be pd.dataframe
        x: a single variable name for x axis
        y: a list, tuple, 1-d array, or Series of variables to check, should be numerical values onlhy
    Returns:
        A valid pd data frame for plotting
    '''
    # todo: remove different type and na
    for y in ys:
        df[y] = pd.to_numeric(df[y], errors='coerce')
    return df.dropna()
