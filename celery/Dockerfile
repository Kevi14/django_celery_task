FROM python:3.12

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY celery/worker.sh ./worker.sh
RUN chmod +x ./worker.sh  # Ensure executable permission

CMD ["bash" ,"./celery/worker.sh"]
