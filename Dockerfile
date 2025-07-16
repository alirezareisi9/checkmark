FROM python:3.12
WORKDIR /app


COPY req.txt /app 
#just in case

RUN pip install --upgrade pip
RUN pip install -r req.txt
COPY checkmark1 /app

EXPOSE 8000
# ENTRYPOINT [ "python3" ]
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"] 