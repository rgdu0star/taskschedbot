FROM arm32v7/python:3.7-alpine3.10

COPY bot.py /bot/bot.py
COPY exec.sh /bot/exec.sh

RUN \
    chmod +x /bot/exec.sh && \
    apk add --update --no-cache python3 tzdata cmd:pip3 && \
    pip3 install --upgrade pip && \
    pip3 install pyTelegramBotAPI pyyaml && \
    rm -rf /var/cache/apk/*

CMD ["/bot/exec.sh"]
