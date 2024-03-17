FROM python:3.11

ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY . /code/

# Install dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8000"]