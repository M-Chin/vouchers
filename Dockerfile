FROM python:3.7-slim

RUN pip3 install pipenv

ENV PROJECT_DIR /usr/src/vouchers

WORKDIR ${PROJECT_DIR}

COPY Pipfile .
COPY Pipfile.lock .
COPY . .

RUN pipenv install --deploy --ignore-pipfile

EXPOSE 5000

CMD ["pipenv", "run", "python", "api.py"]