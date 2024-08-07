---
Title: Балансировка в HAProxy на основе данных cAdvisor
Date: 2015-04-15
Tags: [HAProxy, cAdvisor, Python, Программирование]
Slug: haproxy-cadvisor
Url: it/haproxy-cadvisor
Categories: [IT, Russian]
Build:
  List: local
---

Для запуска Docker-контейнеров у меня в данный момент выделено достаточно много
серверов, причем аппаратная часть у некоторых из них отличается
друг от друга. Соответственно, при настройке на чудесном балансировщике
[HAProxy](http://www.haproxy.org/) такого параметра балансировки
как *"вес сервера"*, приходится это различие в аппаратной части учитывать.

Можно, конечно, подобрать значения весов самостоятельно на основе
данных мониторинга, а при появлении нагрузки от соседних Docker-контейнеров
эти веса корректировать, но это не наш метод.

Не так давно я [писал](/it/check-cadvisor) о том, как использую данные из
[cAdvisor](https://github.com/google/cadvisor) для мониторинга нагруженности
контейнеров.

Поскольку у нас уже есть такой чудесный инструмент как cAdvisor, и мы умеем
получать от него показатели утилизации CPU для выбранных контейнеров, то почему
бы нам не выставлять вес серверов бекенда в зависимости от этого показателя?

Именно так я и думал, когда сел писать простой скрипт на Python,
который бы запускался раз в минуту по cron, и с помощью
[socket-команд](http://cbonte.github.io/haproxy-dconv/configuration-1.4.html#9.2)
менял бы вес сервера в балансировке в зависимости от значения нагрузки
на этот сервер, полученного от cAdvisor API.

Результатом моей работы стал скрипт **[haproxy_cadvisor.py](https://github.com/abulimov/haproxy-cadvisor)**,
который делает ровно то, что я описал.

При этом логика выставления весов очень проста:

1. получаем процент использования CPU для всех бекенд-контейнеров и
считаем среднюю нагрузку;
2. для каждого сервера получаем через socket HAProxy текущий вес и
сопоставляем с текущей нагрузкой;
3. для каждого сервера определяем как надо изменить вес в балансировке,
чтобы получить нагрузку, равную посчитанной средней;
4. для каждого сервера выставляем новый вес, изменив его значение на половину
разницы между текущим весом и требуемым весом, чтобы сгладить скачки нагрузки.

В качестве файла с настройками используется простой JSON-файл, в котором
указывается путь к сокету HAProxy, список URL для опрашиваемых сервисов cAdvisor,
название бекенда в HAProxy, для которого будет осуществлятся динамическое
выставление весов серверов, и регулярное выражение для выбора серверов бекенда из
списка алиасов контейнеров, полученного от cAdvisor.

Достоинства получившегося решения:

* Динамическое выставление весов серверов бекенда в зависимости
нагрузки на них;
* Простота кода и использования:
    - конфиг в JSON
    - работа в Python 2.7+ и Python 3.2+
    - кроме стандартной библиотеки Python используется только Requests.
* Устойчивость к отказу cAdvisor - мы меняем веса только для тех серверов, для
которых получены свежие данные по загруженности.

Поскольку скрипт создавался максимально простым, он (на момент написания этой
заметки) обладает и рядом недостатков:

* Сервисы cAdvisor опрашиваются последовательно;
* Один скрипт может контролировать балансировку только одного бекенда в HAProxy;
* Скрипт не поддерживает работу в режиме сервиса и требует запуска по cron.

Также хочу отметить особенность работы этого решения при наличии нескольких
одновременно работающих серверов-балансировщиков. Заключается она в том,
что поскольку скрипты на этих серверах работают независимо, и никакой
информацией не обмениваются, то и веса выставляют независимо. Это может
привести к ситуации, когда на одном HAProxy для сервера будет выставлен
минимально возможный вес 1, а на втором вес существенно больший среднего.
На работу балансировки это конечно не влияет, поскольку итоговая нагрузка
получается требуемой, но этот момент следует иметь в виду.
Ну и в случае выхода одного из балансировщиков из строя, второму потребуется
пара минут на выравнивание нагрузки.

Описанный скрипт работает у меня в бою уже достаточно продолжительное время,
и отлично себя зарекомендовал. И что интересно - уже после создания этого
решения, читая про [Prometheus](http://prometheus.io/) я обнаружил
[статью от boxever.com](http://www.boxever.com/balancing-based-on-utilisation-with-haproxy),
в которой описан аналогичный подход, однако сам итоговый продукт они
почему-то не выложили.

Я же очень люблю OpenSource, и поэтому описанный в этой заметке скрипт доступен
всем желающим под лицензией MIT в [репозитории на Github](https://github.com/abulimov/haproxy-cadvisor).
