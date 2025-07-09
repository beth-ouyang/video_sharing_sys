FROM python:3.12

RUN apt-get update
COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app
COPY ./backend /app/backend
COPY ./client_page /app/client_page
COPY ./manager_page /app/manager_page
CMD ["python"]