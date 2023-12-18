# Aris Robotics Demo Site

## Setup
- Make sure `data_imutable.csv` is in the ``backend/data/`` folder.
- Run the __poster_scraper.py__ file from project root. See [Data set](#data) for more info.
- To start the services run `docker compose up`.
	- Make sure files are not created as root user, otherwise use chmod to enable read/write to the db.
	`sudo chmod -R go+w ./backend/data/db`
- ``exec`` into the mongodb container and run the import.sh file, to import the data from data.csv into the db.
	- `docker exec mongodb_container bash -c "./import.sh`
	- The reason this *can't* be done as CMD argument, is that the mongodb service has to be fully running first. 
- The website should now be running on http://localhost:8080/

## Frontend

I'm using Dash Bootstrap Components (dbc) as the main building blocks.

### Bootstrap theme

Quartz

### Layout

I'm using the `dbc.Stack` for a horizontally scrolling site, and `dbc.Card` for contextual elements.

### Future considerations

- Adding several pages by routing.
- OAuth by using Flask `LoginManager`.

## Backend

The backend is simply the ``mongodb/mongodb-community-server:6.0-ubi8`` image straight from [dockerhub](https://hub.docker.com/r/mongodb/mongodb-community-server).

It uses a volume that is mounted to `backend/data/db`, which means if you stop and re-run the docker compose command, the whole database is still available as before, and you don't have to re-download and scrape for posters, or convert the csv to mongodb.

## <a id="data"></a>Data set

I've chosen a dataset about books. The headers include author, title, thumbnail (link), rating, number of pages etc.

https://www.kaggle.com/datasets/abdallahwagih/books-dataset/

I plan to show graphs of crossing some of the different columns, to maybe conclude on what genre/length/etc. might be most popular, based on rating.

I saved the dataset in `backend/data/data_imutable.csv`. The scraper then modifies the .csv and saves it in ``backend/data/data`.csv``.

I'm fetching all the images and saving them in the MongoDB locally as base64 encoded strings, and serving them from there instead of as links, like they are in the original data. *Why? to make sure I demonstrate image storage & transfer.*

The __poster_scraper.py__ takes a semi long time to execute, because it isn't threaded for optimum downloading.
Therefore I've added a print statement to it, that updates every 20 downloads. It looks like this:

```1600 / 6810  | =======                        | when_the_lion_feeds_2006.0.jpg```

## Serving / Hosting

I've containerized both front- and backend, using __Docker__ and __Dockercompose__.

## Case

Lav en simpel hjemmeside i __Python__ med __Dash__ frameworket, hvor brugeren skal logge ind med følgende credentials:

Brugernavn: __jonas__

Adgangskode: __admin2023__

Brug en __MongoDB__ database til at hoste data.

Efter brugeren er logget ind, skal der hentes data fra databasen, som præsenteres på en side i Dash appen.

Brug gerne __Pandas__ og __Plotly__.

Du bestemmer selv datamængde og format.

Det hele må gerne være served lokalt.
