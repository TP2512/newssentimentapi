FROM python:3.11

ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY . /code/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir
MAINTAINER  TarkeshP

EXPOSE 8000

CMD ["uvicorn","code.fastapi_app.main:app","--host","0.0.0.0","--port","8000"]