import dash
from dash import html
from layouts import create_layout
from callbacks import register_callbacks

# Define tus keywords, referencia y período aquí
KEYWORDS = ['Forever Chemicals', 'PFOA', 'PFOS', 'Toxic chemicals', 'Water contamination', 'Cancer risk', 'Endocrine disruptors']
REFERENCE = 'pfas'
PERIOD = 'today 5-y'

app = dash.Dash(__name__, suppress_callback_exceptions=True)

app.layout = create_layout()
register_callbacks(app, KEYWORDS, REFERENCE, PERIOD)

if __name__ == '__main__':
    app.run_server(debug=True)