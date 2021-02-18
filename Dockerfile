FROM python:3.8.1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY . /code/
RUN pip install -r requirements.txt
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]