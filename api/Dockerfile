FROM python:3.8

WORKDIR /api

RUN apt-get -y update && apt-get install -y libzbar-dev

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "api/main.py"]