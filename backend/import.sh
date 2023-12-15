#! /bin/bash

mongoimport --db my_db --collection books --type csv --file /app/data/data.csv --headerline --ignoreBlanks