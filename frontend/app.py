from dash import dash, dcc, html, Output, Input, callback, ctx, State
import dash_bootstrap_components as dbc
from pymongo import MongoClient
from os import environ
import pandas as pd

# TODO OAuth basic_auth
# TODO Connect mongodb // pymongo https://pymongo.readthedocs.io/en/stable/tutorial.html

# Init dash app
app = dash.Dash(external_stylesheets=[dbc.themes.QUARTZ, dbc.icons.FONT_AWESOME], update_title=None)
app.title = "Aris Demo"

# Create MongoDB connection
try:
	mongodb_url = environ['MONGODB_URI']
except:
    mongodb_url = 'mongodb://localhost:27017'
    
mongo_client = MongoClient(mongodb_url)
books_db = mongo_client['my_db']['books']

app.layout = dbc.Container(
    [
		dcc.Location(id='url', refresh=False),
        dbc.Stack(
			[
				dbc.Card(
					[
						html.H4(["Entries in Books database: ",
							html.Span(className="card-text", id="count-text"),
               			], className="card-title, m-0"),
      				],
					body=True
				),
    			dbc.Input(placeholder="Search...", type="text", id="search-input"),
				dbc.Button("Get books", className="fw-bold", outline=True, color="primary", id="get-entries-btn", n_clicks=0),
			],
			gap=3
		),
        dbc.Stack(
			gap=3,
			id="result-stack",
   			className="mx-4 pb-3"
		)
	],
    class_name="d-flex flex-column gap-3 pt-3",
)

def get_value_from_object(obj: any, value: str):
    res = ''
    try:
        res = obj[value]
    except:
        pass
    return res

@callback(
	Output('result-stack', 'children'),
	Output('search-input', 'valid'),
	Output('search-input', 'invalid'),
	Input('get-entries-btn', 'n_clicks'),
	State('search-input', 'value'))
def get_entries(click, search_string):
	if click is None or click == 0:
		return []
	if search_string is None or len(search_string) == 0:
		return [], False, True
	try:
		data = list(books_db.find({'title': {'$regex': search_string, '$options': 'i'}}, ['title', 'authors','published_year','average_rating','description']))
	except:
		return []
		# Should show error message to user
  
	print(data)
	return_data = []
	for row in data:
		return_data.append(dbc.Card([
            html.H4(f"{get_value_from_object(row,'title')}", className="card-title"),
            html.Div([
            	html.H6(f"{get_value_from_object(row,'authors')} - {str(get_value_from_object(row,'published_year')).split('.')[0]}",
                     className="card-subtitle",
                     style={'width': 'fit-content'}
                ),
                html.H6([
                    html.I(className="fas fa-star me-1", style={'color': '#FFCD3D'}),
                    f"{get_value_from_object(row, 'average_rating')}"
                    ],
                	className="card-subtitle")
            	],
				className="d-flex flex-row gap-2"
            ),
			html.P(f"{get_value_from_object(row, 'description')}",
                className="card-text",
            )],
			body=True
		))
	return return_data, True, False

@callback(
    Output('count-text', 'children'),
	Input('url', 'pathname'))
def get_count(click):
	return books_db.count_documents({})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080')