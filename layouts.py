from dash import dcc, html

def create_layout():
    return html.Div([
        html.H1("Google Trends Analysis: PFAS and Environmental Health", className='header'),
        html.Div([
            dcc.Graph(id='main-trend-graph', className='main-graph')
        ], className='graph-container'),
        html.Div([
            dcc.Graph(id=f'individual-graph-{i}', className='individual-graph') 
            for i in range(7)  # 7 keywords excluding reference
        ], className='individual-graphs-container')
    ], className='dashboard-container')