FROM python:alpine

WORKDIR /workdir

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY app ./app

ENTRYPOINT ["python", "app/fill_short_time_form.py"]