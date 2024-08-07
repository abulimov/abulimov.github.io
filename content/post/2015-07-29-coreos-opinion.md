---
Title: Впечатления от CoreOS
Date: 2015-07-29
Tags: [CoreOS, Мнение]
Slug: coreos-opinion
Url: it/coreos-opinion
Categories: [IT, Russian]
Build:
  List: local
---

На волне популярности контейнерной виртуализации [Docker](http://docker.com)
стали появляться специализированные дистрибутивы Linux, созданные специально
для использования в роли базового хоста для Docker-контейнеров.

Пионером среди них стал проект [CoreOS](http://coreos.com), затем появились
[Project Atomic](http://www.projectatomic.io/) от RedHat и
[Ubuntu Snappy](https://developer.ubuntu.com/en/snappy/) от Canonical.

Чем они все отличаются от привычных дистрибутивов? Основным отличием является
модель обновления дистрибутива. Все эти проекты предлагают атомарные обновления,
подразумевающие сборку нового образа системы с последующей перезагрузкой в него.
При этом образ монтируется в read-only режиме, и есть возможность откатиться на
предыдущий образ системы. Также приятной особенностью могут быть дополнительные
инструменты для управления контейнерами или кластеризации.

Поскольку мы уже активно используем Docker на базе Ubuntu 14.04 LTS, было
логичным попробовать специализированный дистрибутив для работы с контейнерами,
и выбрал я для этого эксперимента CoreOS. Выбор этот был обусловен отчасти
тем, что в рамках проекта CoreOS было разработано несколько весьма интересных
программ - это **[etcd](https://github.com/coreos/etcd)** и
**[fleet](https://github.com/coreos/fleet)**. Первый из них является
распределенным key-value хранилищем, аналогом Consul, а второй представляет
собой инструмент для оркестрации кластера Docker-хостов путем распределения
через etcd [юнит-файлов systemd](http://www.freedesktop.org/software/systemd/man/systemd.service.html).

В общем, на сайте и в документации все это выглядело весьма интересно, и я с
энтузиазмом ринулся осваивать новые технологии. Реальность же ожидаемо оказалась
весьма печальной - все описанное на сайте (кроме атомарных обновлений) работало
через раз, а иногда и вообще не работало.

Чего стоит только fleet, который всего-то должен раскладывать по хостам
юнит-файлы systemd, и следить за их статусом. Мало того, что он запускает эти
сервисы в блокируещем режиме, так что получить статус кластера в момент запуска
service-файла, который делает docker pull, невозможно, так банальный запуск
трех инстансов одного сервиса на кластере из трех машин закончился тем, что
один из этих трех сервисов остался в inactive состоянии, и вывести его из этой
комы мне не удалось ни многократным пересозданием и уничтожением этого сервиса,
ни ручной очисткой данных etcd.

При этом на аналогичном втором тестовом кластере запуск того же
сервиса на трех нодах прошел успешно, но etcd на всех серверах регулярно сыпал
невнятными ошибками и перезапускался, в результате чего fleet регулярно терял ноды.

И что самое забавное, такое же поведение я наблюдал в начале года на официальном
тестовом проекте [CoreOS-Vagrant](https://github.com/coreos/coreos-vagrant),
но не придал этому значения, списав все на маломощные виртуалки и тестовый
характер окружения. Прошло пол-года, а CoreOS 717.3.0 страдает все от тех
же детских проблем.

Зато атомарные обновления работают вполне исправно, и на том спасибо.
То есть для замены Ubuntu в качестве базового хоста CoreOS подходит.
*Тут стоит сделать одну важную оговорку - при условии, что этот хост крутится
в какой-либо системе виртуализации, в облаке или в KVM/VMware/Xen. Все
дистрибутивы для контейнеров ориентированны именно на такой режим работы.*
Подобная замена даст автоматические атомарные обновления и свежее ядро, и
сократит время на перезагрузки благодаря минималистичной системе.

Но раз главные фичи CoreOS оказались не готовы к нормальной эксплуатации, можно
поэкспериментировать с другими аналогичными системами. А общее впечатление от
CoreOS осталось у меня определенно негативным - нельзя про *такой* уровень
работоспособности писать *такие* вещи:
> The Stable channel should be used by production clusters.
> Versions of CoreOS are battle-tested within the Beta and Alpha channels before being promoted.
> -- https://coreos.com/releases/

По моим впечатлениям, до *production clusters* этому проекту еще расти и расти,
хотя концепция и маркетинг отличные.
