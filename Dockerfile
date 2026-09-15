# 1. Use the official lightweight Python image
FROM python:3.12-slim

# 2. Set environment variables to optimize Python behavior inside Docker
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Set the working directory inside the container
WORKDIR /app

# 4. Copy only requirements first to leverage Docker's caching mechanism
COPY requirements.txt /app/

# 5. Upgrade pip and install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 6. Copy the rest of your Django project code into the container
COPY . /app/

# 7. Expose the port Django will run on
EXPOSE 8000

# 8. Define the default command to start the server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
