# PDF rendering application
This is a simple service for converting PDF files into normalized PNG images. The API accepts PDF douments, then it processes it asynchronously and when the result is ready, you can download finished PNG images. Normalized image means, that it will shrink in size to fit into a 1200x1600 px rectangle without changing its aspect ratio.

Application uses `Flask` (with Connexion) for REST API, tasks are handled by `dramatiq` running with `rabbitmq` backend, and `Postgresql` database is used for storing information about documents. Files are stored directly in filesystem (mounted as external volume to docker).

## How to run
Run all docker containers and expose API on port 8080
```
docker-compose up --build
```

API will be available at [http://localhost:8080/](http://localhost:8080/)

## Configuration

Configuration can be done via `.env` file.

- `DB_DSN` **required** url for connecting to database. E.g. `postgresql://postgres:postgres@db/pdfrenderer` for using default docker db container.
- `DEBUG=true` for enabling debug logs.
- `PATH_DOCUMENTS` and `PATH_IMAGES` to set where to store uploaded and processed files. Must correspond to volume mountings.
- `MAX_UPLOAD_SIZE_BYTES` default 20 MB, set maximum size of uploaded files.
- `RABBIT_HOST`, `RABBIT_DEFAULT_USER` and `RABBIT_DEFAULT_PASS` if you want to use different RabbitMq service than the default docker container.

Also different mounting points for volumes can be set in `docker-compose.yaml`.

**TIP:** By default in docker-compose volume for persistent Postgresql data is set as `external=True`. This means that the volume must be already present to be used. If you don't have any, remove this parameter when running for the first time, so that new volume is created.

## How to use

Easiest usage is via [Swagger UI](http://localhost:8080/ui).

Available endpoints:

- `/upload` - upload PDF document to start processing.
- `/status/{document_id}` - get the status of processing and number of pages in document.
- `/result/{document_id}` or `/result/{document_id}/{page}` - to get the whole result or specific page.

## How to run tests

**Required** postgresql instance. You can use the one that is in docker-compose. It's enough to adjust `DB_DSN` environment variable. Database name must end with `_test` to make sure you don't destroy production database. 2 examples:

### - Run locally:
```
pip install -r requirements.txt
export DB_DSN=postgresql://postgres:postgres@localhost:5432/pdfrenderer_test
python -m pytest --cov src test
```

### - Run in docker
In `.env` set `DB_DSN=postgresql://postgres:postgres@db/pdfrenderer_test`
```
docker-compose run api pytest
```
