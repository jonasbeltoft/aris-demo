#! /bin/bash

mongoimport --host mongodb --db test --collection books --type csv --file /mongo-seed/data.csv --headerline