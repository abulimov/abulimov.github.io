---
Title: Logstash и Graphite
Date: 2015-10-09
Tags: [Graphite, Monitoring, Logstash, StatsD, Опыт]
Slug: logstash-graphite
Url: it/logstash-graphite
Categories: [IT, Russian]
---

Недавно читал серию постов от [Datadog](https://www.datadoghq.com) про сбор метрик,
и в частности [статью про метрики Nginx](https://www.datadoghq.com/blog/how-to-collect-nginx-metrics/)
(думал, вдруг что-то новое узнаю). Что меня в этой статье зацепило - так это то, что только версия
[Nginx Plus](https://www.nginx.com/products/) показывает статистику количества
ответов, разделенную по HTTP-кодам. Поскольку я использую перед Nginx балансировщик
[HAProxy](http://www.haproxy.org), который не жадный и показывает подробную статистику
по кодам ответов для каждого бекенда и фронтенда, я о таком минусе статистики Nginx даже не думал.

Поскольку я совсем недавно решал схожую задачу получения метрик от сервиса,
который сам эти метрики не отдает, решил поделиться достаточно универсальным рецептом,
который поможет, к примеру, получать от обычного Nginx подробную статистику по
кодам ответов.

*Это, на мой взгляд, очень нужная метрика. А то бывает, что сервис твой работает,
мониторинг доволен, а некий процент запросов незаметно падает с 50x ошибками. И вроде бы
можно смотреть в логи в той же Kibana, но не будешь же это делать каждый день.*

###Простой и полезный пример получения метрик из логов

Итак, для приготовления вкусных метрик нам понадобится:

* Некий сервис, который умеет писать логи в любом вменяемом формате, содержащем
интересующие нас метрики. Для примера возьмем обычный Nginx;
* Универсальный комбайн по обработке логов - [Logstash](https://www.elastic.co/products/logstash);
* Агрегатор метрик - [StatsD](https://github.com/etsy/statsd);
* Наконец, сервис хранения метрик - [Graphite](http://graphite.readthedocs.org/en/latest/).

Итак, мы хотим знать, сколько же и каких мы отдаем бедным пользователям HTTP-ответов.
Nginx пишет по-умолчанию access-log в формате *combined*, который определен так:

```nginx
log_format combined '$remote_addr - $remote_user [$time_local] '
                    '"$request" $status $body_bytes_sent '
                    '"$http_referer" "$http_user_agent"';
```

Для нас это отлично, поскольку

1. этот формат совместим с логом Apache2,
2. в этом логе есть нужные нам данные - $status.

Первый пункт радует тем, что не надо писать своих grok-паттернов для Logstash.
Хотя при знании регулярных выражений это и не сложно, всегда лучше взять готовое.

Нужный нам паттерн называется **COMBINEDAPACHELOG**, актуальную версию можно посмотреть
в [репозитории Logstash-plugins](https://github.com/logstash-plugins/logstash-patterns-core/blob/master/patterns/grok-patterns),
на момент написания этой статьи он выглядел так:
```ruby
COMMONAPACHELOG %{IPORHOST:clientip} %{HTTPDUSER:ident} %{USER:auth} \[%{HTTPDATE:timestamp}\] "(?:%{WORD:verb} %{NOTSPACE:request}(?: HTTP/%{NUMBER:httpversion})?|%{DATA:rawrequest})" %{NUMBER:response} (?:%{NUMBER:bytes}|-)
COMBINEDAPACHELOG %{COMMONAPACHELOG} %{QS:referrer} %{QS:agent}
```

*Кстати, в документации к плагину grok указана ссылка на [отличный онлайн-инструмент](http://grokdebug.herokuapp.com)
для проверки grok-паттернов.*

Как мы видим, интересующая нас переменная зовется в Logstash **response**, так что
теперь мы можем спокойно писать конфиг для отправки этой метрики в StatsD->Graphite.
Предположим, мы принимаем логи от Nginx по протоколу syslog (Nginx уже довольно давно
умеет слать логи напрямую в syslog, и это очень удобно).

**пример конфига для парсинга метрик из логов Nginx**
```logstash
input {
  syslog {
    port => 5014
    type => "syslog"
  }
}
filter {
  if [program] == "nginx" {
    grok {
      match => {
        message => '%{COMBINEDAPACHELOG}'
      }
    }
}
output {
  if [type] == "syslog" {
    if [program] == "nginx" {
      # отправим в StatsD количество переданных байт
      statsd {
        host => 'graphite.example.com'
        count => [ "nginx.response_%{response}.bytes", "%{bytes}" ]
        sender => "%{logsource}"
      }
      # увеличим в StatsD счетчик ответов с конкретным кодом
      statsd {
        host => 'graphite.example.com'
        increment => "nginx.response_%{response}"
        sender => "%{logsource}"
      }
    }
    # тут сохраняем логи в elasticsearch, или еще что-то полезное делаем с логами
  }
}
```

Вот и все, открываем [Grafana](http://grafana.org/) и наслаждаемся вкусными
метриками, без всякого Nginx Plus.

#### Мало кому полезный пример из личного опыта

Я решал другую, более специфичную и немного более сложную задачу - получение
времени ответа, количества запросов, переданного объема данных с зависимостью от
статуса попадания в кеш в продвинутом кешируещем
сервере [Apache Traffic Server](http://trafficserver.apache.org).

Тут пришлось чуть больше поработать:

* Написать свой grok-паттерн для парсинга логов ATS
```ruby
TRAFFICSERVER_ACCESS %{NUMBER:ats_timestamp}\s+%{NUMBER:request_msec:int} %{IPORHOST:client_ip} %{WORD:cache_result}/%{NUMBER:http_status_code:int} %{NUMBER:bytes_read:int} %{WORD:http_verb} (%{URIPROTO:http_proto}://)?%{IPORHOST:dst_host}(?::%{POSINT:port:int})?(?:%{URIPATHPARAM:http_request})? %{DATA:cache_user} %{WORD:request_route}/(%{IPORHOST:forwarded_to}|-) %{GREEDYDATA:content_type}
```
* Научить rsyslog тейлить и слать логи ATS в Logstash
```
$MaxMessageSize 32k
$ModLoad imfile

$InputFileName /var/log/trafficserver/squid.log
$InputFileTag trafficserver-access:
$InputFileStateFile trafficserver-access
$InputFileFacility local4
$InputFileSeverity info
$InputRunFileMonitor

local4.* @log.example.com:5014
& ~
```
* Написать конфиг Logstash для отправки полученных метрик в StatsD
```
input {
  syslog {
    port => 5014
    type => "syslog"
  }
}
filter {
  if [program] =~ /trafficserver.+access/ {
    grok {
      patterns_dir => [ "/etc/logstash/patterns" ]
      match => [ "message", "%{TRAFFICSERVER_ACCESS}" ]
      add_tag => [ "trafficserver" ]
    }
    date {
      locale => "en"
      timezone => "+03:00"
      match => [ "ats_timestamp", "UNIX" ]
    }
  }
}
output {
  if [type] == "syslog" {
    if [program] =~ /trafficserver.+access/ {
      statsd {
        host => 'graphite.example.com'
        count => [ "trafficserver.response_%{http_status_code}.%{cache_result}.bytes_read", "%{bytes_read}" ]
        sender => "%{logsource}"
      }
      statsd {
        host => 'graphite.example.com'
        count => [ "trafficserver.response_%{http_status_code}.%{cache_result}.msec", "%{request_msec}" ]
        sender => "%{logsource}"
      }
      statsd {
        host => 'graphite.example.com'
        increment => "trafficserver.response_%{http_status_code}.%{cache_result}"
        sender => "%{logsource}"
      }
    }
  }
}
```

Теперь я могу оценить, насколько медленнее отдаются те запросы, которые не попали
в кеш ATS, и настроить алерты на повышение доли не-20х кодов ответов.

#### Закономерный вопрос

Если [Kibana](https://www.elastic.co/products/kibana) так хороша, и может
строить графики по любым метрикам, зачем же пихать
эти данные в Graphite?

Отвечаю - графики в Kibana это отлично, но очень уж дорого
по ресурсам. Elasticsearch вынужден держать весь индекс в памяти, и в отличие от
Graphite он не может уменьшать разрешение метрик со временем. Так что использование
Graphite позволяет делать алерты по таким метрикам гораздо менее ресурсоемкими,
и хранить метрики несоизмеримо дольше. Ну и весь набор функций Graphite в нашем
распоряжении.
