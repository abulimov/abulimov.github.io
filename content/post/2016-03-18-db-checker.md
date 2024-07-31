---
Title: Открыл код db-checker
Date: 2016-03-18
Tags: [Программирование, Golang, Nagios, Monitoring]
Slug: db-checker
Url: it/db-checker
Categories: [IT, Russian]
Build:
  List: local
---

Недавно я открыл код еще одного инструмента, который уже около года использую на работе -
[db-checker](https://github.com/abulimov/db-checker).

Началось все с необходимости проводить регулярные проверки логической
целостности данных в БД. Проще говоря - гонять мониторингом запросы к базе.

Сначала это была часть проекта, который проверял данные на нашем CDN.
Проект этот сразу планировался многопоточным, поэтому написан на [Go](http://golang.org).
Затем мухи были отделены от котлет, и проверка базы выделилась в отдельную
сущность, но несколько legacy-моментов осталось.

Главной проблемой было то, что проверки определялись в коде, поэтому
добавление новой проверки было относительно нетривиальной задачей,
а код проекта невозможно было сделать открытым. Долгое время у меня не было
времени на устранение этого недостатка, но недавно я взялся за эту задачу.

### db-checker

Результатом стал проект [db-checker](https://github.com/abulimov/db-checker),
который работает как Nagios-совместимый плагин, и позволяет:

* **читать описание проверок из простых [YAML](http://yaml.org)-файлов**
* **делать запросы к PostgreSQL/MySQL и проверять наличие/отсутствие результата**
* **выводить полученные данные в удобной табличной форме**
* **сохранять состояние прошлой проверки и выводить алерты только для новых проблем**

Пройдемся по каждому пункту отдельно.

#### Читать описание проверок из простых [YAML](http://yaml.org)-файлов

Я очень люблю [YAML](http://yaml.org) как формат для конфигов, и описание
проверок в нем выглядят крайне лаконично и просто (примеры в следующем пункте).
При этом хранение проверок отдельно от инструмента очень удобно и дает возможность
очень легко добавлять новые проверки любому человеку.

Все описание проверки состоит всего из 3х обязательных полей:

* query: любой SQL-запрос
* description: Описание проверки
* assert: что мы ожидаем от результата выполнения запроса, *present* или *absent*

#### Делать запросы к PostgreSQL/MySQL и проверять наличие/отсутствие результата

Все проверки целостности данных в базе можно выразить
в форме SQL-запроса, который либо возвращает ОК в случае пройденной проверки,
и тогда мы проверяем *наличие* данных в ответе на запрос, либо мы запрашиваем
список того, чего быть не должно, и тогда мы проверяем *отсутствие* данных
в ответе на запрос, а при наличии - выводим их в отчете.

Например, наличие блокировок в PostgreSQL можно проверять так:

```yaml
query: |
    SELECT
      COALESCE(blockingl.relation::regclass::text,blockingl.locktype) as locked_item,
      (now() - blockeda.query_start)::time AS waiting_duration,
      blockeda.pid AS blocked_pid,
      blockeda.query as blocked_query, blockedl.mode as blocked_mode,
      blockinga.pid AS blocking_pid, blockinga.query as blocking_query,
      blockingl.mode as blocking_mode
    FROM pg_catalog.pg_locks blockedl
    JOIN pg_stat_activity blockeda ON blockedl.pid = blockeda.pid
    JOIN pg_catalog.pg_locks blockingl ON(
      ( (blockingl.transactionid=blockedl.transactionid) OR
      (blockingl.relation=blockedl.relation AND blockingl.locktype=blockedl.locktype)
      ) AND blockedl.pid != blockingl.pid)
    JOIN pg_stat_activity blockinga ON blockingl.pid = blockinga.pid
      AND blockinga.datid = blockeda.datid
    WHERE NOT blockedl.granted;
description: Locks in database
assert: absent
```

Таким образом, если блокировок нет - все отлично, а если есть - выводим их список.

Другой пример - проверка успешных задач `job_name` PGAgent за 4 часа:

```yaml
query: |
    SELECT jlgstatus
    FROM pgagent.pga_joblog
    WHERE jlgstart > (now() - interval '4 hours') AND jlgstatus = 's' AND
    jlgjobid=(
    SELECT jobid FROM pgagent.pga_job WHERE jobname = 'job_name'
    )
    ORDER BY jlgstart DESC LIMIT 1;
description: Не было успешных запусков job_name за прошедший час
assert: present
```

В этом случае мы ждем, что Query вернет нам список задач, а если нет - алерт.

#### Выводить полученные данные в удобной табличной форме

Поскольку сообщения из алертов читают люди, надо показывать проблему так, чтобы
сразу было все понятно, поэтому ASCII-таблица с проблемными значениями подходит
как нельзя лучше.

Пример:

```console
nagios@example.com:~$ ./db-checker --dbname movies --dbuser=checker --dbhost=localhost --dbpassword=SomePassword --checks /opt/checks/movies --critical
CRITICAL:
* Found movies with zero duration
N. ¦ column1 ¦ orig_title                ¦ rus_title
1. ¦ 1346    ¦ Midnight Express          ¦ Полуночный экспресс
2. ¦ 2165    ¦ In the Loop               ¦ В петле
3. ¦ 2254    ¦ Sex & Drugs & Rock & Roll ¦ Секс, наркотики и рок-н-ролл
4. ¦ 2534    ¦ Resident Evil: Damnation  ¦ Обитель Зла: Проклятие
```

#### Сохранять состояние прошлой проверки и выводить алерты только для новых проблем

Предположим, у нас есть некая таблица биллинга, в которой содержатся записи
о транзакциях пользователей. Иногда случаются подозрительные повторные платежи,
о каждом из которых стоит слать уведомление, но лишь единожды. При этом
транзакции из таблицы никуда не пропадают. Вот как раз для такого случая
есть `--diff` режим, который позволяет уведомлять только о новых проблемах.

#### Прочие особенности

Поскольку проект написан на Go, грех было не реализовать параллельное выполнение
проверок (настраивается с помощью флага `--concurrent-checks`).

И конечно я постарался весь важный код покрыть тестами.

### Альтернативы

До принятия решения о написании своего велосипеда я изучал уже готовые утилиты.
Самое близкое по функционалу, что я нашел - [check_postgres.pl](https://bucardo.org/check_postgres/check_postgres.pl.html),
монструозный скрипт на Perl с более чем 8k строк кода, зато с возможностью запускать
ограниченное подмножество запросов через `custom_query`. Под мои задачи он не подошел,
но штука впечатляющая.

### Заключение

Больше информации и примеры проверок можно найти в [репозитории проекта](https://github.com/abulimov/db-checker),
код опубликован под лицензией [MIT](http://opensource.org/licenses/MIT).
