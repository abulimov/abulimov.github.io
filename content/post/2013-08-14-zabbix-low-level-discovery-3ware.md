---
Title: Низкоуровневое обнаружение в Zabbix, ищем диски в контроллере от 3ware
Date: 2013-08-14
Tags: [Zabbix, Python, Monitoring]
Categories: [IT, Russian]
Slug: Низкоуровневое-обнаружение-в-zabbix-ищем-диски-в-контроллере-от-3ware
Url: it/Низкоуровневое-обнаружение-в-zabbix-ищем-диски-в-контроллере-от-3ware
---

Я уже [ писал ](/it/Низкоуровневое-обнаружение-в-zabbix) про [низкоуровневое обнаружение](https://www.zabbix.com/documentation/ru/2.0/manual/discovery/low_level_discovery)
в Zabbix, так что повторять теорию не буду.

Теперь мне понадобилось автоматом получать список хардов в массивах
на контроллерах 3ware, которыми оборудованы у нас многие сервера.

Вести руками шаблоны для каждого сервера с иным порядком или количеством дисков
показалось мне плохой идеей, да и авто-обнаружение само напрашивалось.

Вдохновлялся я утилитой 3ware-status, для работы авто-обнаружения нам потребуется
установленная утилита tw-cli, взять ее для Debian/Ubuntu проще всего [ здесь ](http://hwraid.le-vert.net/).

Работает скрипт примерно так:

1. Получаем общую информацию командой `tw-cli info`, вычленяем оттуда список
   контроллеров простенькой регуляркой `^c[0-9]+$`
2. Получаем информацию для каждого контроллера `tw-cli %controller info`, опять-таки
   регуляркой `^[p][0-9]+$` вытаскиваем оттуда список хардов
3. Отдаем полученный список в формате JSON
4. Используем полученные данные в шаблонах заббикса, в разделе *обнаружение*,
   чтобы вытащить статусы каждого диска в массиве с помощью 3ware-status или tw-cli

На выходе должны получить что-то вроде этого:

    :::json
    {
      "data": [
        {"{#3WARE_DISK}": "c0u0p0"},
        {"{#3WARE_DISK}": "c0p0u1"},
        {"{#3WARE_DISK}": "c0p1u2"},
        {"{#3WARE_DISK}": "c0p1u3"}
      ]
    }

Реализовано все на Python, благо он есть по-умолчанию практически в любом дистрибутиве.

**3ware_discovery.py**

    :::python
    #!/usr/bin/env python
    # -*- coding: utf-8 -*-
    #
    import subprocess
    import sys
    import json
    import re

    binary_path = "/usr/sbin/tw-cli"

    def _run(cmd):
        # returns (rc, stdout, stderr) from shell command
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, shell=True)
        stdout, stderr = process.communicate()
        return (process.returncode, stdout, stderr)

    def _fail(msg):
        print(msg)
        sys.exit(1)

    def parse_controllers(data):
        controllers = []
        for line in data.splitlines():
            if line:
                splitted = line.split()
                if re.match(r'^c[0-9]+$', splitted[0]):
                    controllers.append(splitted[0])
        return controllers

    def parse_disks(data, controller):
        disks = []
        for line in data.splitlines():
            if line:
                splitted = line.split()
                if re.match(r'^[p][0-9]+$', splitted[0]):
                    # '-' means the drive doesn't belong to any array
                    # If is NOT PRESENT too, it just means this is an empty port
                    if not splitted[2] == '-' and not splitted[1] == 'NOT-PRESENT':
                        disks.append({
                            '{#3WARE_DISK}': controller + splitted[2] + splitted[0]
                        })
        return disks

    def main():
        disks_list = []

        rc, raw_data, err = _run("%s info"%binary_path)
        if rc != 0:
            _fail("tw-cli command failed with %s "%err)
        controllers_list = parse_controllers(raw_data)

        for controller in controllers_list:
            rc, raw_data, err = _run("%s info %s"%(binary_path, controller))
            if rc != 0:
                _fail("tw-cli command failed with %s "%err)
            disks_list.extend(parse_disks(raw_data, controller))

        data = {
            'data': disks_list
        }
        print json.dumps(data)

    if __name__ == "__main__":
        main()


Ну и конечно нужно создать ключ, по которому заббикс будет список дисков получать.

В конфиге заббикса добавляем строку вида

    UserParameter=3ware.discovery,sudo /opt/3ware_discovery.py

В этом случае, нужно беспарольное sudo на эту команду для пользователя Zabbix.

Ну а в самом заббиксе уже создаем в шаблоне обнаружение, в котором используем ключ
3ware.discovery и макрос {#3WARE\_DISK}, например 3ware.disk\_status[{#3WARE\_DISK}].
Подробности - в документации.

Исходники доступны в моем [репозитории](https://github.com/abulimov/utils), в папке *`zabbix/data_collectors`*.
