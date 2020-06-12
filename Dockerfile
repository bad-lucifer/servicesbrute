FROM python:3.6.4

ADD . /app

WORKDIR /app

EXPOSE 8082

RUN apt-get update \
    && apt-get install -y software-properties-common \
    && add-apt-repository ppa:pi-rho/security \
    && apt-get install -y hydra \
    && apt-get install -y nmap \
    && pip install -r requirements.txt \
    && chmod +x run_celery.sh \
    && adduser --disabled-password --gecos '' celery_user

CMD ["gunicorn", "main:app", "-c", "gunicornConfig.py"]