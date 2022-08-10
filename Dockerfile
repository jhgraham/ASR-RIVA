# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

#install dependencies that aren't copied with pip
RUN apt-get update -y && apt-get install -y --no-install-recommends build-essential gcc \
                                        libsndfile1 

# Install pip requirements
COPY requirements.txt /code/requirements.txt
COPY riva_api-2.3.0-py3-none-any.whl /code/riva_api-2.3.0-py3-none-any.whl

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#RUN pip install /code/riva_api-2.3.0-py3-none-any.whl

WORKDIR /code
COPY ./app /code/app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
#RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
#USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
