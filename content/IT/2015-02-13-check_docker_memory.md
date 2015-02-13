Title: Научился мониторить использование памяти в Docker-контейнерах
Date: 2015-02-13
Tags:   Python, Nagios, Icinga2
Category: IT
Slug: check-docker-memory

Я сегодня занимался мониторингом, а конкретно нашими докер-контейнерами. 

*Лирическое отступление:
Для мониторинга я теперь (уже на другом месте работы) использую
наследника Nagios - [Icinga2](https://www.icinga.org/icinga/icinga-2/). 
Пока все нравится, ребята очень круто переписали Nagios, реализовали гораздо
более вменяемый формат конфигурации, и кучу новых возможностей.*

Используя Docker для автотестов я уже ловил проблемы, когда интерпретатор Ruby
кушал всю выделенную память в контейнере и тихо умирал от рук OOM Killer.

Поскольку теперь я использую [Docker](http://docker.io) уже не только для тестов,
но и "в бою", меня сильно беспокоило то, что мы не можем мониторить
использование памяти внутри контейнера.
А не можем мы этого делать потому, что все утилиты (free, top) и плагины мониторинга
используют данные из /proc/meminfo, которые внутри контейнеров 
[не актуальны](http://fabiokung.com/2014/03/13/memory-inside-linux-containers/).

К сожалению, на сегодняшний день проблема мониторинга памяти изнутри контейнера
так пока никем и не решена, хотя пожеланий у людей много, и [работа ведется](https://github.com/docker/docker/issues/8427).

Ну а раз проблему нельзя решить изнутри, надо пробовать решать ее снаружи - так я подумал,
и решил посмотреть, как получить данные по использованию памяти для Docker-контейнера на хосте, который его запустил.

Тут все весьма неплохо - для старых версий Docker можно было смотреть статистику
в `/sys/fs/cgroup/memory/lxc/$CID/memory.stat`, где $CID это наш Container ID.
В новых версиях, использующие native драйвер, ту же информацию можно получить из
`/sys/fs/cgroup/memory/docker/$CID/memory.stat`.

Осталось только эти данные красиво прикрутить к мониторингу.

Поскольку я уже настроил в Icinga2 зависимости для виртуалок от родительских хостов,
как описано [в официальной документации](http://docs.icinga.org/icinga2/latest/doc/module/icinga2/chapter/monitoring-basics#dependencies),
у каждой виртуалки в `host.vars.vm_parent` прописан родитель, то есть
описание шаблона для хоста выглядит примерно так:

    template Host "generic-docker-host-on-vm01" {
      import "generic-docker-host"
      vars.vm_parent = "vm01"
    }

Это дает нам возможность для проверки памяти значение `nrpe_address` брать
из `host.vars.vm_parent`, то есть описание сервиса выглядит так:

    apply Service "memory-docker" {
      import "generic-service-nrpe"
      display_name = "Memory Usage in Docker"
      vars.nrpe_address = host.vars.vm_parent
      vars.nrpe_command = "check_docker_memory"
      vars.nrpe_arguments = [
        host.name,
        15,
        10
      ]
      assign where host.vars.vm_parent
    }

Таким образом, проверка относится к виртуалке, но выполняется
на родительском хосте. А раз относится к виртуалке - то зависит от ее живости, и когда виртуалка в DOWN, лишних алертов не будет. Да и вообще - все логично, проверка памяти хоста относится к самому хосту.

Такое вот довольно элегантное решение получилось.

Ну и, в завершение статьи, сам скрипт проверки - **check_docker_memory.py**, написан для Python 2.7+, без внешних зависимостей,
[взять можно тут](https://github.com/abulimov/utils/blob/master/nagios/check_docker_memory.py).

Пример использования check_docker_memory.py - проверим, что количество свободной памяти в контейнере
loving_lalande не меньше, чем 15%, и уж точно не меньше 10%:

    :::bash
    nagios@hostname:~$ ./check_docker_memory.py -n loving_lalande -w 15 -c 10 -f
    CheckDockerMemory OK: 89.005% (6533008 kB) free! | TOTAL=7340032KB;;;; USED=807024KB;;;; FREE=6533008KB;;;;
