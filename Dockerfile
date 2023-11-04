FROM python:3.11

SHELL ["/bin/bash", "-c"]

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8001

RUN pip install --upgrade pip

RUN apt update && apt -qy install gcc libjpeg-dev libxslt-dev \
libpq-dev libmariadb-dev libmariadb-dev-compat gettext cron openssh-client flake8 locales


RUN useradd -rms /bin/zsh host_api && chmod 777 /opt /run

WORKDIR /host_api
RUN mkdir /host_api/static && mkdir /host_api/media
RUN chown -R host_api:host_api /host_api && chmod 755 /host_api

COPY --chown=host_api:host_api . .

RUN pip install -r requirements.txt

USER host_api

CMD ["gunicorn", "-b", "0.0.0.0:8000", "--workers", "4", "--threads", "2", "core.wsgi:application"]
