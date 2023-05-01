ARG SPARK_VERSION="v3.4.0"
FROM apache/spark-py:$SPARK_VERSION

USER 0

RUN mkdir /app

ARG MSCOCO_SOURCE=https://huggingface.co/datasets/ChristophSchuhmann/MS_COCO_2017_URL_TEXT/resolve/main/mscoco.parquet
RUN wget $MSCOCO_SOURCE -O /app/mscoco.parquet

ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

ADD download_imgdataset.py /app/download_imgdataset.py
