FROM python:3.10

WORKDIR /src

COPY . /src/

RUN pip install -r src/requirements.txt

EXPOSE 8080

CMD ["python", 'MovieRecommender.py']