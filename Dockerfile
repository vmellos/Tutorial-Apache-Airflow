FROM apache/airflow:2.2.5-python3.8

USER root

WORKDIR /opt/airflow

ENV PYTHONPATH "${PYTHONPATH}:/opt/airflow"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
COPY .env .

RUN pip install --upgrade pip && pip install -r requirements.txt \
    --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.3.2/constraints-3.7.txt" \
    --no-warn-script-location

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    vim \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


USER airflow