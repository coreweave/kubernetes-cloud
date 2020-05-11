FROM python:3.7-slim

#ARG DEBIAN_FRONTEND=noninteractive
#RUN apt-get update && apt-get install -y build-essential

ENV APP_HOME /app
WORKDIR $APP_HOME

# Install production dependencies.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r ./requirements.txt

# Copy local code to container image
COPY main.py ./

ENTRYPOINT ["python", "main.py"]
