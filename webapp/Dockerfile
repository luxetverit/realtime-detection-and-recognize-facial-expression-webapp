FROM python:3.9.16

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
CMD ["bash", "-c", "python manage.py collectstatic --settings=webapp.settings.deploy --no-input"]
#EXPOSE 8000
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
