from datetime import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from flask_caching import Cache
import pandas as pd
import numpy as np
from helper import Helper
from definitions import *

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    'https://fonts.googleapis.com/css?family=Work+Sans'
]

# Create app object
app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets
)
app.title = 'Dashboard | Auto Loans'

# Set up cache. Required since dataset for each trust is quite large
cache = Cache()
cache_params = {'CACHE_TYPE': 'filesystem', 'CACHE_DIR': 'cache'}
cache.init_app(app.server, config=cache_params)

# PLOTS
# Create Graph objects here. Nothing much here. All action happens inside update functions below
main_scatter_plot = dcc.Graph(id='main-scatter-plot')
main_histogram = dcc.Graph(id='main-histogram')
main_heatmap = dcc.Graph(id='main-heatmap')
main_map = dcc.Graph(id='main-map')
main_evo = dcc.Graph(id='main-evo')

# FILTERS
# Define left column filters

# Scatter plot filters
msp_filters = html.Div([
    html.Div([
        'Axis Y:',
        dcc.Dropdown(
            id="msp-yaxis",
            options=[{'label': i, 'value': i} for i in msp_axes],
            value="Interest Rate (%)")
    ],
        className='filter-elem'),
    html.Div([
        'Axis X:',
        dcc.Dropdown(
            id="msp-xaxis",
            options=[{'label': i, 'value': i} for i in msp_axes],
            value="Credit Score"
        )
    ],
        className='filter-elem'),
    dcc.Checklist(
        id='msp-nonperf',
        options=[
            {'label': 'Show Non-performing', 'value': 'D'},
            {'label': 'Show Repossessed', 'value': 'R'},
        ],
        values=[],
        className='filter-elem'
    )
],
    className='filter-area'
)

# Histogram filters
hg_filters = html.Div([
    html.Div([
        'Histogram for:',
        dcc.Dropdown(
            id="hg-xaxis",
            options=[{'label': i, 'value': i} for i in hg_axes],
            value="Interest Rate (%)")
    ], className='filter-elem'),
    html.Div([
        'Include:',
        dcc.RadioItems(
            id='hg-nonperf',
            className='filter-elem',
            options=[
                {'label': 'All', 'value': 'A'},
                {'label': 'Non-performing', 'value': 'D'},
                {'label': 'Repossessed', 'value': 'R'}
            ],
            value='A')
    ], className='filter-elem'),
    html.Div([
        'Desired no of bins:',
        dcc.Slider(
            id='hg-bins',
            className='filter-elem',
            min=5,
            max=50,
            value=20,
            marks={
                5: '5',
                20: '20',
                50: '50',
            },
            included=False,
            disabled=False)
    ], className="filter-elem")
],
    className='filter-area'
)

# Heatmap filters
hm_filters = html.Div([
    html.Div([
        'Axis Z (color):',
        dcc.Dropdown(
            id="hm-zaxis",
            options=[{'label': i, 'value': i} for i in hm_zaxis],
            value="Interest Rate (%)"
        )
    ],
        className='filter-elem'),
    html.Div([
        'Axis Y:',
        dcc.Dropdown(
            id="hm-yaxis",
            options=[{'label': i, 'value': i} for i in hm_axes],
            value="Payment-to-Income Percentage")
    ],
        className='filter-elem'),
    html.Div([
        'Axis X:',
        dcc.Dropdown(
            id="hm-xaxis",
            options=[{'label': i, 'value': i} for i in hm_axes],
            value="Credit Score"
        )
    ],
        className='filter-elem'),
],
    className='filter-area'
)

# Map filters
map_filters = html.Div([
    html.Div([
        'Metric:',
        dcc.Dropdown(
            id="map-metric",
            options=[{'label': i, 'value': i} for i in map_metrics],
            value="Interest Rate (%) - Avg.")
    ], className='filter-elem'),
],
    className='filter-area'
)

# Delinquent loan evolution chart filters
evo_filters = html.Div([
    html.Div([
        'Metric:',
        dcc.Dropdown(
            id='evo-metric',
            options=[
                {'label': 'Total Count', 'value': 'Total count'},
                {'label': 'Total Value', 'value': 'Total value'}],
            value="Total count")
    ], className='filter-elem'),
    html.Div([
        'Include:',
        dcc.Checklist(
            id='evo-nonperf',
            className='filter-elem',
            options=[
                {'label': 'Non-performing', 'value': 'D'},
                {'label': 'Repossessed', 'value': 'R'}
            ],
            values=['D', 'R'])
    ], className='filter-elem')
],
    className='filter-area'
)


# LAYOUT
# Create dashboard layout
app.layout = html.Div(
    id='main',
    children=[
        # Header title
        dcc.Markdown(id='trust_title',
                     children=loading_string,
                     className='main-title'),
        # Manufacturer and trust select boxes
        html.Div([html.Div([
            dcc.Dropdown(
                id="manu_select",
                options=[{'label': m, 'value': m} for m in list(trusts.keys())],
                value='Toyota'),
            dcc.Dropdown(
                id="trust_select",
                options=[{'label': t['name'], 'value': t['cik']} for t in trusts['Toyota']],
                value="1694919")
            ], className='')
        ], className='top-select'),
        # Tabs
        dcc.Tabs(id="tabs",
                 children=[
                     dcc.Tab(
                         label="Scatter plots",
                         children=[html.Div([msp_filters], className='left-column'),
                                   html.Div([main_scatter_plot], className='right-column')],
                         className='main-tab'
                     ),
                     dcc.Tab(
                         label="Histograms",
                         children=[html.Div([hg_filters], className='left-column'),
                                   html.Div([main_histogram], className='right-column')],
                         className='main-tab'
                     ),
                     dcc.Tab(
                         label="Heat maps",
                         children=[html.Div([hm_filters], className='left-column'),
                                   html.Div([main_heatmap], className='right-column')],
                         className='main-tab'
                     ),
                     dcc.Tab(
                         label="Maps",
                         children=[html.Div([map_filters], className='left-column'),
                                   html.Div([main_map], className='right-column')],
                         className='main-tab'
                     ),
                     dcc.Tab(
                         label="Evolution",
                         children=[html.Div([evo_filters], className='left-column'),
                                   html.Div([main_evo], className='right-column')],
                         className='main-tab'
                     ),
                     dcc.Tab(
                         label="About",
                         children=[html.Div([], className='left-column'),
                                   dcc.Markdown(
                                       id='about-text',
                                       children=[],
                                       className='right-column  plain-text')],
                         className='main-tab'
                     )
                 ]
                 ),
        # Hidden signal div. Required to send signal to update functions when dataset changes
        html.Div(id='signal', style={'display': 'none'}, children="")
    ]
)


# UPDATES

# Extract data from either cache or database
@cache.memoize()
def get_data(trust_cik):
    return Helper.load_autoloans_by_cik([trust_cik])


# Update trust dropdown when manufacturer dropdown value changes
@app.callback(
    dash.dependencies.Output('trust_select', 'options'),
    [dash.dependencies.Input('manu_select', 'value')]
)
def update_trust_options(manu_name):
    return [{'label': t['name'], 'value': t['cik']} for t in trusts[manu_name]]


# Update signal with new cik when selected trust changes
@app.callback(
    dash.dependencies.Output('trust_select', 'value'),
    [dash.dependencies.Input('manu_select', 'value')]
)
def update_trust_value(manu_name):
    print(manu_name)
    return trusts[manu_name][0]['cik']


# Update text on about tab when trust selection changes (signal updated)
@app.callback(
    dash.dependencies.Output('about-text', 'children'),
    [dash.dependencies.Input('trust_select', 'value')]
)
def update_about_text(cik):
    trust_name = list(filter(lambda t: t['cik'] == cik, trusts_flat))[0]['name']

    return about_text.format(trust_name)


# Update page title on trust change. "Loading..." indicator does not work properly [TBD]
@app.callback(
    dash.dependencies.Output('trust_title', 'children'),
    [dash.dependencies.Input('signal', 'children'),
     dash.dependencies.Input('trust_select', 'value')]
)
def update_title(signal_cik, select_cik):
    if not select_cik == signal_cik:
        return loading_string
    else:
        trust_name = list(filter(lambda t: t['cik'] == signal_cik, trusts_flat))[0]['name']
        return f'## {trust_name}'


# Update dataset and send signal upon selection of new trust by the user
@app.callback(
    dash.dependencies.Output('signal', 'children'),
    [dash.dependencies.Input('trust_select', 'value')])
def update_dataset(cik):
    # Compute value and send a signal when done
    get_data(cik)
    return cik


# Update scatter plot
@app.callback(
    dash.dependencies.Output('main-scatter-plot', 'figure'),
    [dash.dependencies.Input('msp-xaxis', 'value'),
     dash.dependencies.Input('msp-yaxis', 'value'),
     dash.dependencies.Input('msp-nonperf', 'values'),
     dash.dependencies.Input('signal', 'children')]
)
def update_msp(xaxis_column_name, yaxis_column_name, non_perf, cik):
    df = get_data(cik)

    trace = go.Scattergl(
        x=df[xaxis_column_name],
        y=df[yaxis_column_name],
        mode='markers',
        marker=dict(
            size=3,
            color=colors['green'],
            opacity=0.5
        ),
        hoverinfo='none'
    )

    traces = [trace]

    if 'D' in non_perf:
        trace_d = go.Scattergl(
            x=df[df['30 Days Delinquency Date'].notnull()][xaxis_column_name],
            y=df[df['30 Days Delinquency Date'].notnull()][yaxis_column_name],
            mode='markers',
            marker=dict(
                size=5,
                color=colors['amber'],
                opacity=0.8
            ),
            hoverinfo='none'
        )
        traces.append(trace_d)

    if 'R' in non_perf:
        trace_r = go.Scattergl(
            x=df[df['Repossession Date'].notnull()][xaxis_column_name],
            y=df[df['Repossession Date'].notnull()][yaxis_column_name],
            mode='markers',
            marker=dict(
                size=5,
                color=colors['red'],
                opacity=0.8
            ),
            hoverinfo='none'
        )
        traces.append(trace_r)

    layout = go.Layout(
        # title=f'<b>{yaxis_column_name} vs. {xaxis_column_name}</b>',
        # titlefont = {'size': 16},
        font=dict(family=font_family, size=14),
        height=550,
        margin={'t': 50, 'r': 20},
        xaxis=dict(
            title=f'<b>{xaxis_column_name}</b>',
            showline=True,
            mirror=True,
            ticks='outside',
            zeroline=False,
            tickformat=Helper.get_format(xaxis_column_name)
        ),
        yaxis=dict(
            title=f'<b>{yaxis_column_name}</b>',
            showline=True,
            mirror=True,
            ticks='outside',
            zeroline=False,
            tickformat=Helper.get_format(yaxis_column_name)
        ),
        showlegend=False,
    )

    return {'data': traces, 'layout': layout}


# Update histogram
@app.callback(
    dash.dependencies.Output('main-histogram', 'figure'),
    [dash.dependencies.Input('hg-xaxis', 'value'),
     dash.dependencies.Input('hg-nonperf', 'value'),
     dash.dependencies.Input('hg-bins', 'value'),
     dash.dependencies.Input('signal', 'children')]
)
def update_hg(xaxis_column_name, non_perf, bins, cik):
    df = get_data(cik)

    hg_data = df[xaxis_column_name]
    bar_color = colors['green']
    if non_perf == 'D':
        hg_data = df[df['30 Days Delinquency Date'].notnull()][xaxis_column_name]
        bar_color = colors['amber']
    elif non_perf == 'R':
        hg_data = df[df['Repossession Date'].notnull()][xaxis_column_name]
        bar_color = colors['pink']

    # Certain fields need to be sorted
    order_sequence = None
    if xaxis_column_name in categorical_fields:
        order_sequence = df[xaxis_column_name].value_counts().index

    layout = go.Layout(
        title=f'<b>{xaxis_column_name} Distribution</b>',
        xaxis=dict(
            # title=xaxis_column_name,
            ticks='outside',
            zeroline=False,
            showline=True,
            categoryorder=('array' if order_sequence is not None else 'trace'),
            categoryarray=(order_sequence if order_sequence is not None else []),
            tickformat=Helper.get_format(xaxis_column_name)
        ),
        font=dict(family=font_family, size=14),
        height=550,
    )

    trace = go.Histogram(
        x=hg_data,
        nbinsx=int(bins),
        # autobinx=False,
        marker=dict(
            color=bar_color,
            opacity=0.8
        )
    )

    traces = [trace]

    return {'data': traces, 'layout': layout}


# Disable no of bins slider for categorical fields
@app.callback(
    dash.dependencies.Output('hg-bins', 'disabled'),
    [dash.dependencies.Input('hg-xaxis', 'value')])
def disable_hg_bins_slider(metric):
    return True if metric in categorical_fields else False


# Update heatmap
@app.callback(
    dash.dependencies.Output('main-heatmap', 'figure'),
    [dash.dependencies.Input('hm-xaxis', 'value'),
     dash.dependencies.Input('hm-yaxis', 'value'),
     dash.dependencies.Input('hm-zaxis', 'value'),
     dash.dependencies.Input('signal', 'children')]
)
def update_hm(xaxis_column_name, yaxis_column_name, zaxis_column_name, cik):
    df = get_data(cik)

    # Create new data subset and assign axes
    subdata = pd.DataFrame({
        'x': df[xaxis_column_name],
        'y': df[yaxis_column_name],
    })
    if zaxis_column_name in countable_metrics:
        subdata['z'] = subdata.index
    elif zaxis_column_name in delinquency_metrics:
        subdata['z'] = df[delinquency_metrics[zaxis_column_name]]
    else:
        subdata['z'] = df[zaxis_column_name]
    # Filter out nans
    subdata = subdata[subdata.x.notnull() & subdata.y.notnull()]
    # Cut axes into bins if numeric
    grouped = {'x': False, 'y': False}
    if subdata.x.dtype in numeric_types:
        subdata.x = pd.cut(subdata.x, 20, include_lowest=True)
        grouped['x'] = True
    if subdata.y.dtype in numeric_types:
        subdata.y = pd.cut(subdata.y, 20, include_lowest=True)
        grouped['y'] = True

    # Modify z-axis type because pivot table does not work with float32
    if subdata.z.dtype in ['float16', 'float32']:
        subdata.z = subdata.z.astype('float')
    # Build pivot table
    if zaxis_column_name in countable_metrics:
        pt = pd.pivot_table(subdata, index='y', columns='x', values='z', aggfunc='count', fill_value=0)
    elif zaxis_column_name in delinquency_metrics:
        subdata['ones'] = 1
        pt1 = pd.pivot_table(subdata, index='y', columns='x', values='z', aggfunc='count', fill_value=0)
        pt2 = pd.pivot_table(subdata, index='y', columns='x', values='ones', aggfunc='count', fill_value=0)
        pt1.sort_index(axis=0, inplace=True)
        pt1.sort_index(axis=1, inplace=True)
        pt2.sort_index(axis=0, inplace=True)
        pt2.sort_index(axis=1, inplace=True)
        pt = pt1 / pt2
        pt.sort_index(axis=0, inplace=True)
        pt.sort_index(axis=1, inplace=True)
        pt.fillna(0, inplace=True)
    else:
        pt = pd.pivot_table(subdata, index='y', columns='x', values='z', aggfunc='mean', fill_value=0)
    pt.sort_index(axis=0, inplace=True)
    pt.sort_index(axis=1, inplace=True)

    x_labels = pt.columns
    y_labels = pt.index
    if grouped['x']:
        x_labels = np.array([str((i.left + i.right) / 2) for i in pt.columns])
    if grouped['y']:
        y_labels = np.array([str((i.left + i.right) / 2) for i in pt.index])

    trace = go.Heatmap(
        x=x_labels,
        y=y_labels,
        z=pt.values.tolist(),
        colorscale='Greens',
        reversescale=True,
        colorbar=dict(
            tickformat=Helper.get_format(zaxis_column_name, precision=1)
        ),
    )

    layout = go.Layout(
        font=dict(
            family=font_family,
            size=14),
        autosize=True,
        height=550,
        margin={'t': 50, 'l': 100},
    )

    return dict(data=[trace], layout=layout)


# Update map
@app.callback(
    dash.dependencies.Output('main-map', 'figure'),
    [dash.dependencies.Input('map-metric', 'value'),
     dash.dependencies.Input('signal', 'children')])
def update_map(metric_raw, cik):
    df = get_data(cik)
    # Extract metric name from its label
    metric = metric_raw.split(" - ")[0].strip()
    if metric in countable_metrics:
        state_data = df['Geographic Location'].value_counts()
    elif metric in delinquency_metrics:
        metric_dfname = delinquency_metrics[metric]
        state_data = df[df[metric_dfname].notnull()][['Geographic Location', metric_dfname]] \
            .groupby('Geographic Location').agg('count')
        state_data['Total'] = df['Geographic Location'].value_counts()
        state_data[metric] = state_data[metric_dfname] / state_data['Total']
        state_data = state_data[metric]
    else:
        state_data = df.groupby('Geographic Location')[metric].mean()

    map_data = dict(
        type="choropleth",
        # colorscale='Greens',
        colorscale=list(zip(np.linspace(0, 1, len(colorscales['green'])), colorscales['green'])),
        reversescale=True,
        autocolorscale=False,
        locations=state_data.index,
        z=state_data.values,
        locationmode='USA-states',
        marker=dict(
            line=dict(
                color='#fff',
                width=2
            )
        ),
        colorbar=dict(
            tickformat=Helper.get_format(metric, precision=1)
        ),
    )
    # Text and formatting for hover text
    if metric in percentage_fields:
        map_data['hoverinfo'] = 'text+location'
        map_data['text'] = [Helper.get_format(metric, precision=1, style='python').format(v) for v in state_data.values]
    else:
        map_data['hoverinfo'] = 'text+location'
        map_data['text'] = [Helper.get_format(metric, precision=0, style='python').format(v) for v in state_data.values]

    map_layout = go.Layout(
        # title=f'<b>{metric_raw} By State</b>',
        geo=dict(
            scope='usa',
            projection=dict(type='albers usa'),
            showlakes=True,
            lakecolor='rgb(255, 255, 255)'
        ),
        font=dict(family=font_family, size=14),
        autosize=True,
        height=550,
        margin=dict(l=0, r=0, t=50, b=0),
    )

    return dict(data=[map_data], layout=map_layout)


# Update evolution chart
@app.callback(
    dash.dependencies.Output('main-evo', 'figure'),
    [dash.dependencies.Input('signal', 'children'),
     dash.dependencies.Input('evo-metric', 'value'),
     dash.dependencies.Input('evo-nonperf', 'values')])
def update_evo(cik, metric, nonperf):
    df = get_data(cik)

    # Date range for date axis
    min_date = df['First Filing Date'].min()
    max_date = datetime.today()
    x_axis = Helper.get_months(min_date, max_date)
    # Compute totals
    total_count = [len(df) for _ in x_axis]
    total_value = [df['Loan Amount ($)'].sum() for _ in x_axis]
    # Counts
    rep_count = np.array([df[df['Repossession Date'] <= t]['Repossession Date'].count() for t in x_axis])
    del_count = np.array([df[(df['30 Days Delinquency Date'] <= t) &
                             (df['Repossession Date'].isnull())]['30 Days Delinquency Date'].count() for t in x_axis])
    rep_countdiff = np.insert(np.diff(rep_count), 0, 0)
    del_countdiff = np.insert(np.diff(del_count), 0, 0)
    # Percentages
    rep_countper = rep_count / total_count
    del_countper = del_count / total_count
    # Value-based
    rep_val = np.array([df[df['Repossession Date'] <= t]['Loan Amount ($)'].sum() for t in x_axis])
    del_val = np.array([df[(df['30 Days Delinquency Date'] <= t) &
                             (df['Repossession Date'].isnull())]['Loan Amount ($)'].sum() for t in x_axis])
    rep_valdiff = np.insert(np.diff(rep_val), 0, 0)
    del_valdiff = np.insert(np.diff(del_val), 0, 0)
    # Percentages
    rep_valper = rep_val / total_value
    del_valper = del_val / total_value

    # Assign axes
    if metric == 'Total count':
        y_1 = del_count
        y_2 = rep_count
        y_1d = del_countdiff
        y_2d = rep_countdiff
        y_1p = del_countper
        y_2p = rep_countper
    else:
        y_1 = del_val
        y_2 = rep_val
        y_1d = del_valdiff
        y_2d = rep_valdiff
        y_1p = del_valper
        y_2p = rep_valper

    trace_1 = dict(
        name='Non-performing',
        x=x_axis,
        y=y_1,
        type='line',
        line=dict(
            color=colors['amber'],
            width=5
        )
    )
    trace_2 = dict(
        name='Repossessed',
        x=x_axis,
        y=y_2,
        type='line',
        line=dict(
            color=colors['red'],
            width=5
        )
    )

    trace_1d = dict(
        name='Non-perf Change',
        x=x_axis,
        y=y_1d,
        type='bar',
        line=dict(
            color=colors['amber']
        )
    )

    trace_2d = dict(
        name='Repo Change',
        x=x_axis,
        y=y_2d,
        type='bar',
        line=dict(
            color=colors['red']
        )
    )

    traces = []
    if 'D' in nonperf:
        traces.append(trace_1)
        traces.append(trace_1d)
    if 'R' in nonperf:
        traces.append(trace_2)
        traces.append(trace_2d)

    layout = go.Layout(
        font=dict(
            family=font_family,
            size=14),
        autosize=True,
        height=550,
        margin={'t': 50, 'l': 100},
        xaxis=dict(
            showline=True,
            mirror=True,
            ticks='outside',
            zeroline=False
        ),
        yaxis=dict(
            title=f'<b>{metric}</b>',
            showline=True,
            mirror=True,
            ticks='outside',
            zeroline=False,
            tickformat=Helper.get_format(metric)
        ),
        showlegend=True,
        legend=dict(
            orientation='h'
        )
    )

    return dict(data=traces, layout=layout)


if __name__ == '__main__':
    app.run_server(debug=True)
