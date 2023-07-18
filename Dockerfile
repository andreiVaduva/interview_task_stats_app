FROM python:3.10

# Set the working directory.
WORKDIR /app

# Copy the backend requirements.
COPY ./requirements.txt /app/requirements.txt

# Install the requirements.
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Uncomment the line below to copy the backend source code inside the docker image.
# COPY ./backend /app/backend

# The command used to start the backend inside the docker container.
CMD ["uvicorn", "backend.main:app", "--reload", "--host", "0.0.0.0", "--port", "80"]
