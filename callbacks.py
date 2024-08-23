from dash.dependencies import Input, Output
import plotly.graph_objects as go
from data_processing import get_trends_data_with_reference, get_individual_data_with_reference

def register_callbacks(app, keywords, reference, period):
    @app.callback(
        [Output('main-trend-graph', 'figure')] +
        [Output(f'individual-graph-{i}', 'figure') for i in range(len(keywords))],
        Input('main-trend-graph', 'id')
    )
    def update_graphs(_):
        data = get_trends_data_with_reference(keywords, reference, period)
        individual_data = get_individual_data_with_reference(keywords, reference, period)

        main_fig = create_main_figure(data, keywords)
        individual_figs = [create_individual_figure(individual_data, keyword, reference) for keyword in keywords]

        return [main_fig] + individual_figs

def create_main_figure(data, keywords):
    fig = go.Figure()
    for keyword in keywords:
        fig.add_trace(go.Scatter(x=data.index, y=data[keyword], mode='lines', name=keyword))
    fig.update_layout(
        title='Trends Comparison',
        xaxis_title='Date',
        yaxis_title='Relative Interest',
        template='plotly_white',
        hovermode='x unified'
    )
    return fig

def create_individual_figure(data, keyword, reference):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data[keyword], mode='lines', name=keyword))
    fig.add_trace(go.Scatter(x=data.index, y=data[reference], mode='lines', name=reference, line=dict(dash='dash')))
    fig.update_layout(
        title=f'{keyword} vs {reference}',
        xaxis_title='Date',
        yaxis_title='Interest',
        template='plotly_white',
        hovermode='x unified',
        showlegend=False
    )
    return fig