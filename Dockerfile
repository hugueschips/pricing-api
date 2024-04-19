FROM python:3.12-slim

LABEL maintainer="Daniel Durrenberger <lhommelepluscl@ssedumon.de>"

RUN apt-get update && apt-get install -y build-essential curl git && apt-get clean
RUN pip install --no-cache-dir "uvicorn[standard]==0.23.2" "gunicorn==21.2.0"

# COPY ./docker/start.sh /start.sh
# RUN chmod +x /start.sh

# COPY ./docker/gunicorn_conf.py /gunicorn_conf.py

# COPY ./docker/start-reload.sh /start-reload.sh
# RUN chmod +x /start-reload.sh

ENV PYTHONPATH "${PYTHONPATH}:/"
ENV PORT=8080

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python3 - --version 1.6.1 && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy using poetry.lock* in case it doesn't exist yet
COPY ./pyproject.toml ./poetry.lock* /app/

WORKDIR /app/

RUN poetry install --only main

COPY ./src /app

EXPOSE 8081

# Run the start script, it will check for an /app/prestart.sh script (e.g. for migrations)
# And then will start Gunicorn with Uvicorn
# CMD ["/start.sh"]

# Start the app without start.sh file
CMD ["uvicorn", "pricing.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
# CMD poetry run start
