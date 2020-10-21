FROM python:3

WORKDIR /usr/src/app

RUN pip install psycopg2
RUN pip install kaggle
RUN pip install pandas
RUN pip install SQLAlchemy
COPY ./kaggle.json /root/.kaggle/kaggle.json
RUN kaggle datasets download -d olistbr/brazilian-ecommerce
RUN apt install unzip 
RUN unzip brazilian-ecommerce.zip
COPY ./etl.py /usr/src/app
CMD ["python3", "etl.py"]
 
