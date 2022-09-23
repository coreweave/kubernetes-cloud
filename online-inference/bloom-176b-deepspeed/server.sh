export MODEL_NAME=microsoft/bloom-deepspeed-inference-fp16
export DEPLOYMENT_FRAMEWORK=ds_inference
export DTYPE=fp16

# for more information on gunicorn see https://docs.gunicorn.org/en/stable/settings.html
gunicorn -t 0 -w 1 -b 127.0.0.1:5000 server:app --access-logfile - --access-logformat '%(h)s %(t)s "%(r)s" %(s)s %(b)s'
