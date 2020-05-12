FROM pytorch/pytorch:1.5-cuda10.1-cudnn7-runtime

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y build-essential

ENV APP_HOME /app
WORKDIR $APP_HOME

# Install production dependencies.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r ./requirements.txt

# Copy local code to container image
COPY *.py ./

CMD ["python", "model.py"]
