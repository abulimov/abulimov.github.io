Title: Мониторим Docker-контейнеры с cAdvisor и Nagios/Icinga2
Date: 2015-02-20
Tags:   Python, Nagios, Icinga2, cAdvisor, Monitoring
Category: IT
Slug: check-cadvisor

После того, как я [научился мониторить память в Docker-контейнерах](/it/check-docker-memory),
я решил мониторить еще и нагрузку на CPU.
Поскольку это дело не самое тривиальное, и хотелось не писать свой
велосипед, а пользоваться чем-то популярным и поддерживаемым, я решил
попробовать [cAdvisor](https://github.com/google/cadvisor).

И вот что я могу сказать - отличный инструмент!
Ресурсов практически не потребляет (около 20 Мб оперативной памяти и
неизмеримо мало CPU), обладает простым API для доступа к собираемой им
информации, имеет красивый веб-интерфейс с realtime-графиками.
А еще умеет сам писать метрики в InfluxDB, и в будущем [научится писать
в Graphite](https://github.com/google/cadvisor/issues/474).

Конечно, наличие API позволяет написать плагин для любого мониторинга,
чем я тут же и занялся.

Единственная хитрость была в том, что cAdvisor отдает нам статистику потребления
квантов времени в наносекундах для CPU, и надо это переводить в проценты загрузки.

Формула довольно проста, и найдена в одном из issues к самому cAdvisor:

    Usage % = (Used CPU Time (in nanoseconds) for the interval) /(interval (in nano secs) * num cores)

Вооружившись этим знанием, я написал [плагин check_cadvisor.py](https://github.com/abulimov/utils/blob/master/nagios/check_cadvisor.py),
который умеет проверять использование CPU и оперативной памяти в контейнере через cAdvisor API.

Пример использования check_cadvisor.py - проверим, что количество свободной памяти в контейнере
loving_lalande не меньше, чем 15%, и уж точно не меньше 10%:

    :::bash
    nagios@hostname:~$ ./check_cadvisor.py -u http://cadvisor_url -n loving_lalande -m -w 15 -c 10
    CheckDockerStats OK: 79.96% (5869163 kB) free! | mem_used=1470868KB;1101004;734003;0;7340032

А теперь проверим, что CPU используется менее чем на 10%, и уж точно менее, чем на 20%:

    :::bash
    nagios@hostname:~$ ./check_cadvisor.py -u http://cadvisor_url -n loving_lalande -C -w 10 -c 20
    CheckDockerStats WARNING: 12.98% CPU used! | cpu_usage=12.98%;10;20;0;100

Поскольку мой плагин отдает perfdata, а Icinga2 умеет слать ее в Graphite,
я могу не ждать добавление отправки в Graphite к cAdvisor, и уже сейчас получать графики
использования ресурсов в контейнерах.

Можно еще прикрутить проверки использования места на подключенных дисках - cAdvisor эти данные тоже
собирает. Но мне пока такие проверки без надобности.
