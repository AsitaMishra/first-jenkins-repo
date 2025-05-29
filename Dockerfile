FROM python:3.11-slim

WORKDIR /

COPY . .

RUN pip install -e . --no-cache-dir

RUN python3 -m pipeline.build_pipeline

EXPOSE 8080

CMD [ "python3", "app.py" ]