# ./docker/Dockerfile
FROM python:3.11
# specifying the working directory inside the container
WORKDIR $HOME

# installing the Python dependencies
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# copying the contents of our app' inside the container
COPY . .

# defining env vars
ENV FLASK_APP=app.app
# watch app' files
ENV FLASK_DEBUG=true
ENV FLASK_ENV=development

COPY migrations $HOME/migrations

# running Flask as a module, we sleep a little here to make sure that the DB is fully instanciated before running our app'
CMD  ["flask", "db", "upgrade"]
CMD ["flask", "run", "--host=0.0.0.0", "--port=5010"]
