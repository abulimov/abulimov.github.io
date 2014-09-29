Title: Низкоуровневое обнаружение в Zabbix
Date: 2013-06-26
Tags: Zabbix, Python
Category: IT
Slug: Низкоуровневое-обнаружение-в-zabbix

В используемой мной системе мониторинга Zabbix, начиная с версии 2.0,
появилась такая любопытная штука, как [низкоуровневое обнаружение](https://www.zabbix.com/documentation/ru/2.0/manual/discovery/low_level_discovery)

Я не буду пересказывать содержимое документации, расскажу лучше о том, как я писал свой тип
обнаружения для мониторинга очередей RabbitMQ.

Проблема в том, что очередей в RabbitMQ может быть много, и, по мере развития веб-проекта,
они меняются. Так что я решил обнаруживать их автоматически, и написал для этого свой провайдер
данных для обнаружения заббикса.

Порядок действий прост:

1. Получаем список vhostов командой `rabbitmqctl -q list_vhosts name`
2. Получаем для каждого vhost список очередей командой `rabbitmqctl -q list_queues -p %vhost name`
3. Отдаем полученные пары vhost:queue в формате JSON
4. Используем полученные данные в шаблонах заббикса, в разделе *обнаружение*
5. PROFIT!

На выходе должны получить что-то вроде этого:

    :::json
    {
      "data": [
        {"{#RABBITMQ_VHOST_NAME}": "/", "{#RABBITMQ_QUEUE_NAME}": "hello"},
        {"{#RABBITMQ_VHOST_NAME}": "/", "{#RABBITMQ_QUEUE_NAME}": "world"}
      ]
    }

Реализовано все на Python, код предельно прост, в комментариях не нуждается.

**rabbitmq_discovery.py**

    :::python
    #!/usr/bin/env python
    # -*- coding: utf-8 -*-

    import subprocess
    import sys
    import json

    def _run(cmd):
        # returns (rc, stdout, stderr) from shell command
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, shell=True)
        stdout, stderr = process.communicate()
        return (process.returncode, stdout, stderr)

    def parse_vhosts(data):
        vhosts = []
        for line in data.splitlines():
            vhosts.append(line.strip())
        return vhosts

    def parse_stat(data, vhost):
        stat = []
        for line in data.splitlines():
            stat.append({
                '{#RABBITMQ_VHOST_NAME}': vhost,
                '{#RABBITMQ_QUEUE_NAME}': line.strip(),
            })
        return stat

    def _fail(msg):
        print(msg)
        sys.exit(1)


    def main():
        rc, raw_data, err = _run("rabbitmqctl -q list_vhosts name")
        if rc != 0:
            _fail("rabbitmqctl command failed with %s "%err)
        vhosts = parse_vhosts(raw_data)

        raw_stats = []
        for vhost_name in vhosts:
            rc, raw_data, err = _run("rabbitmqctl -q list_queues -p %s name"%vhost_name)
            if rc != 0:
            _fail("rabbitmqctl command failed with %s "%err)
            raw_stats = raw_stats + parse_stat(raw_data, vhost_name)

        data = {
            'data': raw_stats
        }
        print json.dumps(data)

    if __name__ == "__main__":
        main()

Еще нужно создать ключ, по которому заббикс будет всю эту красоту получать.

В конфиге заббикса добавляем что-либо вида

    UserParameter=rabbitmq.discovery,sudo /opt/rabbitmq_discovery.py

В моем случае, нужно беспарольное sudo на эту команду для пользователя zabbix.

Ну а в самом заббиксе уже создаем в шаблоне обнаружение, в котором используем ключ
rabbitmq.discovery и макросы {#RABBITMQ\_VHOST\_NAME} и {#RABBITMQ\_QUEUE\_NAME}.
Это подробно описано в документации,
так что я этого описывать не буду.

Исходники доступны в моем [репозитории](https://github.com/abulimov/utils), в папке *zabbix/data\_collectors*.
