from dash import dash, dcc, html, Output, Input, callback, ctx, State
import dash_bootstrap_components as dbc
from pymongo import MongoClient
from os import environ
import pandas as pd
import plotly.express as px

# TODO OAuth basic_auth

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
						html.H4("Distribution of Published Years", className="card-title"),
						html.Div(id="year-dist-result"),
						dcc.Loading(
								type="default",
								children=html.Div(id="loading-output-year-hist")
						),
      				],
					body=True
				),
				dbc.Card(
					[
						html.H4("Correlation between Average Rating and Number of Pages", className="card-title"),
						html.Div(id="rating-corr-result"),
						dcc.Loading(
								type="default",
								children=html.Div(id="loading-output-rating-corr")
						),
      				],
					body=True
				),
				dbc.Card(
					[
						html.H4("Top Categories by Amount", className="card-title"),
						html.Div(id="categories-result"),
						dcc.Loading(
								type="default",
								children=html.Div(id="loading-output-categories")
						),
      				],
					body=True
				),
				dbc.Card(
					[
						html.H4("Average rating per year", className="card-title"),
						html.Div(id="avg-rating-result"),
						dcc.Loading(
								type="default",
								children=html.Div(id="loading-output-avg-rating")
						),
      				],
					body=True
				),
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
        dcc.Loading(
            type="dot",
            children=html.Div(id="loading-output")
        ),
        dbc.Stack(
			gap=3,
			id="result-stack",
   			className="mx-4 pb-3"
		)
	],
    class_name="d-flex flex-column gap-3 pt-3",
)


@callback(
    Output("avg-rating-result", "children"),
    Output("loading-output-avg-rating", "children"),
    Input('url', 'pathname'))
def year_dist(url):
	try:
		df = pd.DataFrame(list(books_db.find(projection=['published_year', 'average_rating'])))
		
  		# Group by published year and calculate the average rating for each year
		average_rating_by_year = df.groupby('published_year')['average_rating'].mean().reset_index()

		# Create a line plot
		fig = px.line(average_rating_by_year, x='published_year', y='average_rating',
            template="plotly_dark", color_discrete_sequence =['#83c79a'])
		fig.update_layout(xaxis_title='Published Year', yaxis_title='Average Rating')
		return dcc.Graph(figure=fig), ''
	except:
		fig = px.scatter()
		return dcc.Graph(figure=fig), ''

@callback(
    Output("categories-result", "children"),
    Output("loading-output-categories", "children"),
    Input('url', 'pathname'))
def year_dist(url):
	try:
		df = pd.DataFrame(list(books_db.find(projection=['categories'])))
		
  		# Make the figure
		top_categories = df['categories'].str.split(', ', expand=True).stack().value_counts().nlargest(10).reset_index()
		top_categories.columns = ['Category', 'Book Count']
		# Flip the plot
		top_categories = top_categories.iloc[::-1]

		fig = px.bar(top_categories, y='Book Count', x='Category', orientation='v',
			template="plotly_dark", color_discrete_sequence =['#83c79a'],
            labels={'Book Count': 'Number of Books', 'Category': 'Categories'})
		return dcc.Graph(figure=fig), ''
	except:
		fig = px.scatter()
		return dcc.Graph(figure=fig), ''

@callback(
    Output("rating-corr-result", "children"),
    Output("loading-output-rating-corr", "children"),
    Input('url', 'pathname'))
def year_dist(url):
	try:
		df = pd.DataFrame(list(books_db.find(projection=['num_pages','average_rating'])))
		
  		# Make the figure
		fig = px.scatter(df, x='average_rating', y='num_pages',
			template="plotly_dark", color_discrete_sequence =['#83c79a'],
            labels={'average_rating': 'Average Rating', 'num_pages': 'Number of Pages'})
		return dcc.Graph(figure=fig), ''
	except:
		fig = px.scatter()
		return dcc.Graph(figure=fig), ''

@callback(
    Output("year-dist-result", "children"),
    Output("loading-output-year-hist", "children"),
    Input('url', 'pathname'))
def year_dist(url):
	try:
		df = pd.DataFrame(list(books_db.find(projection=['published_year'])))
		# Make the figure
		fig = px.histogram(df, x='published_year', nbins=20,
			template="plotly_dark", color_discrete_sequence =['#83c79a']
   		)
		fig.update_layout(xaxis_title='Published Year', yaxis_title='Number of Books')
		return dcc.Graph(figure=fig), ''
	except:
		fig = px.histogram()
		return dcc.Graph(figure=fig), ''

def get_value_from_object(obj: any, value: str):
    res = ''
    try:
        res = obj[value]
    except:
        pass
    return res

@callback(
	Output('result-stack', 'children'),
	Output('loading-output', 'children'),
	Output('search-input', 'valid'),
	Output('search-input', 'invalid'),
	Input('get-entries-btn', 'n_clicks'),
	State('search-input', 'value'))
def get_entries(click, search_string):
	if click is None or click == 0:
		return [], '', None, None
	if search_string is None or len(search_string.strip()) == 0:
		return [], '', False, True
	try:
		data = list(books_db.find(limit=100, filter={'title': {'$regex': search_string, '$options': 'i'}}, projection=['title', 'authors','published_year','average_rating','description', 'thumbnail']))
	except:
		return [], '', None, None
		# Should show error message to user

	# Render output
	return_data = []
	for row in data:
		return_data.append(dbc.Card(dbc.CardBody([
			html.Div([
				html.H4(f"{get_value_from_object(row,'title')}", className="card-title"),
				html.Div([
					html.H6(f"{get_value_from_object(row,'authors').replace(';', ' & ')} - {str(get_value_from_object(row,'published_year')).split('.')[0]}",
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
				)
			]),
			html.Img(src="data:image/jpg;base64," + get_value_from_object(row, 'thumbnail')[2:-1],
				alt="Poster Image",
				height="100%",
				style={'min-height': '200px', 'max-height': '300px'}
            )
		],
		className="d-flex flex-row justify-content-between gap-3"
	)))
	return return_data, '', True, False

# Get amount of entries in db on site load
@callback(
    Output('count-text', 'children'),
	Input('url', 'pathname'))
def get_count(url):
	return books_db.count_documents({})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080')