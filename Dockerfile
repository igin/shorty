FROM python:alpine as application

WORKDIR /workdir

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY app ./app

ENTRYPOINT ["python", "app/fill_short_time_form.py"]

FROM application as test

COPY requirements-dev.txt requirements-dev.txt
RUN pip3 install -r requirements-dev.txt

ENTRYPOINT ["pytest"]
