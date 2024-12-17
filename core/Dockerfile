FROM python:3.12

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /usr/src/app

# Install Django
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the Django project
COPY . .

# Run the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
