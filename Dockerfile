FROM python:3.9
MAINTAINER Andor Kesselman <andor@henosisknot.com>
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./ /code/app
WORKDIR /code/app
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
CMD ["python", "main.py"]
