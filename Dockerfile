FROM registry.echocloud.com/docker/python

ENV APP_ENV=/kitty_watcher/configs/production.yaml

WORKDIR /kitty_watcher

ADD . .

RUN pip install --trusted-host mirrors.aliyun.com -r requirements.txt && \
    pip install -e .

CMD ["/usr/local/bin/gunicorn", "wsgi", "-b", "0.0.0.0:34023", "--workers=4"]

EXPOSE 34023
