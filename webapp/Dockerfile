FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

ENV PYTHONUNBUFFERED 1

RUN apt-get -y update
RUN apt-get -y install vim
RUN apt-get -y install libgl1-mesa-glx

RUN mkdir /code
ADD . /code/

WORKDIR /code
ADD requirements.txt /code/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "webapp.asgi:application", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
#EXPOSE 8000
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
