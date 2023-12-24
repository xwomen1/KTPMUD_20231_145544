FROM python:3.11 as requirements-stage


#Set /tmp as the current working directory. Here's where we will generate the file requirements.txt
WORKDIR /tmp


RUN pip install poetry


# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./pyproject.toml ./poetry.lock* /tmp/


# Generate the requirements.txt file.
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes


FROM python:3.11


WORKDIR /code

COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY ./app /code/app

COPY ./alembic /code/alembic

COPY ./alembic.ini /code




# Run the uvicorn command, telling it to use the app object imported from app.main.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Migration database
CMD ["alembic", "upgrade", "heads"]