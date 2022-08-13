FROM python:3.9-alpine

ENV PATH="/scripts:${PATH}"\
    PYTHONUNBUFFERED=1\
    PYTHONDONTWRITEBYTECODE=1\
    POETRY_VERSION=1.1.2\
    POETRY_NO_INTERACTION=1
    
WORKDIR /genki

# Dependencies
COPY poetry.lock pyproject.toml ./
RUN apk add --update --no-cache --virtual .build-deps gcc libc-dev linux-headers\
    libffi-dev libressl-dev\
    postgresql-dev python3-dev musl-dev\
    && pip install poetry==${POETRY_VERSION}\
    && poetry config virtualenvs.create false\
    && poetry install --no-dev --no-root --extras deployment\
    && apk del --no-cache .build-deps\
    && apk add libpq

# Deployment-specific stuff
COPY ./deployment/scripts /scripts
RUN chmod +x /scripts/*\
    && mkdir -p {/vol/web/media,/vol/web/static}\
    && ln -s /vol/web/media /genki/media\
    && ln -s /vol/web/static /genki/static\
    && adduser -D user\
    && chown -R user:user /vol\
    && chmod -R 755 /vol/web

# Everything else
COPY . .
USER user

CMD ["entrypoint.sh"]
