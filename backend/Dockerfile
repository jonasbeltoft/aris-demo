FROM mongo:3.2.6
RUN mkdir -p /app/data
WORKDIR /app/data
COPY ./data/data.csv /app/data
COPY import.sh /app/data
CMD ["mongod", "&&", "mongoimport", "-db", "test", "-c", "books", "--file", "data.csv", "--headerline"]