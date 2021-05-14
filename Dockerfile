FROM python:3.8.5

WORKDIR /app/

COPY . .

RUN pip3 install -r requirements.txt

WORKDIR /app/tests/

CMD [ "pytest" ]

