from dash import dash, html
import dash_bootstrap_components as dbc

app = dash.Dash(external_stylesheets=[dbc.themes.QUARTZ])

# TODO OAuth basic_auth
# TODO Connect mongodb // pymongo https://pymongo.readthedocs.io/en/stable/tutorial.html

app.layout = dbc.Container(
    [
        dbc.Stack(
			[
				dbc.Card(
					[
						html.H4("Card title", className="card-title"),
						html.P("This is some card text", className="card-text"),
					],
					body=True
				),
				dbc.Card(
					[
						html.H4("Card title", className="card-title"),
						html.P("This is some card text", className="card-text"),
					],
					body=True
				)
			],
			gap=3
		)
	],
    class_name="d-flex pt-3"
)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080')