# Aris Robotics Demo Site

## Frontend

### Bootstrap themes for consideration

 1. Quartz
 2. Darkly
 3. Flatly - Dark mode
 4. Litera - Dark mode
 5. Minty - Dark mode
 
 ## Data set

https://www.kaggle.com/datasets/abdallahwagih/books-dataset/

 I've chosen a dataset about books. The headers include author, title, thumbnail (link), rating, number of pages etc.

 I plan to show graphs of crossing some of the different columnms, to maybe conclude on what genre/length/etc. might be most popular, based on rating.

 I'm going to make use of the MongoDB to fetch all the images locally, and serving them from the DB, instead of as links, like they are in the original data. *Why? to make sure I demonstrate image storage & transfer.*

## Serving / Hosting

I plan to containerize both front- and backend, using __Docker__ and __Dockercompose__, which is now a part of docker.

## Case

Lav en simpel hjemmeside i __Python__ med __Dash__ frameworket, hvor brugeren skal logge ind med følgende credentials:

Brugernavn: __jonas__

Adgangskode: __admin2023__

Brug en __MongoDB__ database til at hoste data.

Efter brugeren er logget ind, skal der hentes data fra databasen, som præsenteres på en side i Dash appen.

Brug gerne __Pandas__ og __Plotly__.

Du bestemmer selv datamængde og format.

Det hele må gerne være served lokalt.