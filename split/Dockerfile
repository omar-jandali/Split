FROM python:3
WORKDIR users
COPY requirements.txt ./
EXPOSE 8000
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
