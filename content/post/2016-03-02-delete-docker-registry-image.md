---
Title: О пользе Python и костылях с Docker
Date: 2016-03-02
Tags: [Программирование, Python, Docker]
Slug: delete-docker-registry-image
Url: it/delete-docker-registry-image
Categories: [IT, Russian]
Build:
  List: local
---

В процессе организации авто-очистки [Docker Registry 2](https://github.com/docker/distribution),
устав ждать в появления в нем столь "ненужного" функционала, как удаление образов
с диска (DELETE запросы удаляют тег, но сами данные остаются на диске и жрут место),
я в очередной раз прибег к помощи скрипта из
[delete-docker-registry-image](https://github.com/burnettk/delete-docker-registry-image),
и уперся в то, что этот самый скрипт (написанный изначально на bash) невероятно
медленно работает на большом Registry.

К примеру, удаления одного тега для repository с 70 тегами, в каждом из которых
много слоев, занимает **49 минут**. А мне надо удалить 60 старых тегов из 70.

Посмотрев на [сам скрипт](https://github.com/burnettk/delete-docker-registry-image/blob/aa2644234840dc31f3afd6a06691aec6aa899cbd/delete_docker_registry_image),
я понял, что проще и быстрее всего будет переписать его на Python, избавившись
от тысяч порождаемых в циклах процессов.

За час была реализована самая простая базовая функциональность, после чего
сравнение производительности показало очень солидное ускорение, так что
портирование продолжилось уже в чистовом варианте.

Процесс переписывания занял меньше одного рабочего дня, и был очень облегчен тем
фактом, что автор изначального скрипта снабдил свое детище
[тестами](https://github.com/burnettk/delete-docker-registry-image/blob/master/test/test).
Я тоже стараюсь писать тесты для важных вещей - без них рефакторинг (особенно в Python
с его динамической типизацией) превращается в ад.

#### Итоги

Версия на Python избавилась от зависимостей bash-скрипта типа jq, работает
на Python 2.7 и 3+, и использует только стандартную библиотеку.
Быстродействие изменилось кардинально -
то же удаление одного тега из 70 стало занимать **30 секунд** против
49 минут в версии на bash.

Конечно, я не преминул вернуть свои изменения в апстрим, так что
теперь более быстрый вариант доступен всем страждущим. Автор изначального
скрипта был крайне рад такому повороту событий.

После этих полезных для общественности действиям вся процедура очистки
моего registry от старых образов выполняется с помощью скрипта
[clean_old_versions.py](https://github.com/burnettk/delete-docker-registry-image/tree/master#clean_old_versionpy),
который лежит в том же репозитории, и который я тоже слегка доработал.

Для меня это отлично - проект продолжает поддерживаться апстримом, а я свою задачу
по очистке Registry выполнил, причем без создания каких-либо внутренних утилит, которые
потом еще придется поддерживать, и принес пользу сообществу - сила OpenSource в действии.

Единственное грустное пятно в этой истории - Docker-registry. Уже версия 2+, переписали
с Python на Go, про Docker трубят все кому не лень, а таких простых вещей как удаление образов - нет,
и приходится городить костыли.