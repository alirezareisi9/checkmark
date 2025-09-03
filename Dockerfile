# FROM python:3.12
# WORKDIR /app


# COPY req.txt /app 
# #just in case

# RUN pip install --upgrade pip
# RUN pip install -r req.txt
# COPY checkmark1 /app

# EXPOSE 8000
# # ENTRYPOINT [ "python3" ]
# CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"] 

FROM python:3.12

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1  # Avoids .pyc files
ENV PYTHONUNBUFFERED 1  # shows logs in real time

# Set working directory inside the container
WORKDIR /code
# the directory in which your application code runs and where commands 
#  are executed. It serves as a default directory for all subsequent 
#  commands, meaning that any relative paths specified in the commands 
#  will be relative to this directory.

COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the rest of your Django project
COPY . /code/

# Collect static files
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "checkmark1.wsgi:application", "--bind", "0.0.0.0:8000"]