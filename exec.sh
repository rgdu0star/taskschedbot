#!/bin/sh
cp /usr/share/zoneinfo/Europe/Moscow /etc/localtime && \
echo "Europe/Moscow" > /etc/timezone

cd /bot
python3 bot.py
