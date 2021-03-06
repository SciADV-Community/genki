FROM python:3.8-alpine

ENV PATH="/scripts:${PATH}"\
    PYTHONUNBUFFERED=1\
    PYTHONDONTWRITEBYTECODE=1\
    POETRY_VERSION=1.1.2\
    POETRY_NO_INTERACTION=1

RUN apk add --update --no-cache --virtual .build-deps gcc libc-dev linux-headers\
    libffi-dev libressl-dev\
    postgresql-dev python3-dev musl-dev
RUN pip install poetry==${POETRY_VERSION}
RUN poetry config virtualenvs.create false
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-dev --no-root --extras deployment
RUN apk del --no-cache .build-deps
RUN apk add libpq

WORKDIR /genki

COPY ./deployment/scripts /scripts
RUN chmod +x /scripts/*

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
RUN ln -s /vol/web/media /genki/media
RUN ln -s /vol/web/static /genki/static
RUN adduser -D user
RUN chown -R user:user /vol
RUN chmod -R 755 /vol/web

COPY . .

USER user

CMD ["entrypoint.sh"]