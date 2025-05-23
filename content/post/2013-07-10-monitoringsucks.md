---
Title: Monitoring sucks!
Date: 2013-07-10
Modified: 2014-06-12
Tags: [Zabbix, Sensu, Monitoring, Мнение]
Categories: [IT, Russian]
Slug: monitoring-sucks
Url: it/monitoring-sucks
Build:
  List: local
---

**TL;DR - тут я Sensu критиковал, но в 2014 году успешно заменил Zabbix на Sensu версии 0.12+**

В 2012 году появился в среде DevOps такой хештег, #monitoringsucks.
В сообщения с этим тегом devopsы писали, что текущее положение дел
в сфере мониторинга их не устраивает. Что именно - прекрасно иллюстрирует
[эта презентация](https://speakerdeck.com/obfuscurity/the-state-of-open-source-monitoring)
Если вкратце - хочется людям некоего стандарта API для взаимодействия между компонентами
утилит мониторинга, ну и появления самих этих компонент, чтоб из них строить
гибкий и умный мониторинг.

Итогом этой волны недовольства стали массовые обсуждения проблем
и привлечение внимания к интересным утилитам типа [Sensu](http://sensuapp.org/)
и [Riemann](http://riemann.io/).

В 2013 году хештег в сообществе сменился - теперь это #monitoringlove.
Произошло это благодаря развитию OpenSource-утилит для мониторинга.
Глядя на всеобщее воодушевление, я решил в рамках эксперимента
отринуть верой и правдой служивший мне 2 года [Zabbix](http://www.zabbix.com),
и попробовать в тех же задачах использовать Sensu.
Riemann я не стал всерьез рассматривать, поскольку на данный момент
у него нет никаких средств для обеспечения отказоустойчивости, да и
сама идея писать конфиг на каком-либо языке программирования (а уж тем более
на Clojure) порочна.

Я сравнил на одних и тех же задачах Sensu и Zabbix.
Задачи простые - мониторинг всего стека приложения для современного веб-сайта,
т.е. Nginx+Unicorn, Riak, Redis, RabbitMQ, Postgres, и сами сервера.
Конечно, все эксперименты я делал на виртуалках, имитирующих реальную площадку.

####Вот минусы и плюсы Sensu версии 0.9 в сравнении с Zabbix версии 2.0.6:

###Минусы Sensu

  * Нет зависимостей между событиями. (UPD 2014 - уже есть).
    Это безусловно главный минус, и как его будут исправлять - неясно.
  * Уведомления куцые по настройкам.
    Это второй по важности минус. Я пробовал его обойти с помощью
    [Flapjack](https://github.com/flpjck/flapjack),
    но поскольку сам Flapjack еще не умеет (хоть и заявляют в целях)
    зависимости между событиями - то толку с него мало.
  * Конфиг в JSON, а не в YAML. (для себя решил генерацией конфига из Ansible).
  * Вся логика содержится в проверочных скриптах.
    (UPD 2014 - сейчас мне это кажется даже плюсом)
  * Нужен внешний хранитель метрик, он же рисователь графиков.
    (UPD 2014 - после графиков Zabbixа, графики Graphite это просто супер)
  * Куцая документация.
    (UPD 2014 - документация стала сильно лучше)
    Хоть и обещают они, что все документировано, но, к примеру, на момент написания
    этой заметки, документации по созданию фильтров нет вообще.
    К счастью, проект простой, можно разобраться, просто читая код.


###Плюсы Sensu

  * Конфиг можно хранить в git.
  * Масштабируемость.
  * Отказоустойчивость.
  * Гибкость выбора системы хранения данных.
  * Поддержка плагинов Nagios.
  * Авто-подключение клиентов.
  * Механизм подписок.
  * Данные публикуются клиентами по мере генерации.


###Минусы Zabbix

  * Настройка через веб-морду.
    Это ужасно, когда я не могу в деплой площадки внести и деплой.
    мониторинга целиком, вместе с конфигом..
  * Конфиги нельзя хранить в git.
  * Масштабируемость только с помощью proxy.
  * Ресурсоемкость.
  * Данные забираются раз в n минут сервером.


###Плюсы Zabbix

  * Зависимости, сложные условия.
  * Внешние скрипты для уведомлений.
  * UserParameter, которые позволяют проверять что угодно..
  * Авто-обнаружение.
  * Низкоуровневое обнаружение.
  * Большое сообщество, много шаблонов и пользовательских данных.
  * Мощная веб-админка.
  * Встроенные обработки данных.
  * Встроенные графики.

По итогу эксперимента могу сказать, что, на мой взгляд, жить c Sensu можно, но затрачивать человекочасы на
доведение мониторинга до ума нужно в огромных объемах, побольше чем в Nagios.
И уж точно еще рано говорить о замене того же Zabbix или Zenoss на что-то модульное
на базе какого-нибудь Sensu+Graphite+Flapjack.

Лично я остаюсь на Zabbix, несмотря на все его недостатки.

**UPD 2014 - я успешно заменил Zabbix на Sensu версии 0.12+ и Graphite**
