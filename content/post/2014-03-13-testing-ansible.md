---
Title: Тестирование Ansible Playbook
Date: 2014-03-13
Tags:  [Ansible, Мнение]
Categories: [IT, Russian]
Slug: Тестирование-ansible-playbook
Url: it/Тестирование-ansible-playbook
Build:
  List: local
---

Давно хотел сделать авто-тестирование целостности развертывания, производимого
с помощью [Ansible](http://ansible.com). Чтобы, значит, запушил я новую версию плейбука в репозитория,
и CI проверила работоспособность системы. Причем не просто корректность синтаксиса,
а работоспособность проводимого деплоя.

Вот наконец до этого дошли руки.

Точнее, руки до этого дошли еще в середине 2013 года, но тогда я собрал все это
с помощью стройной системы костылей, взяв за основу заранее минимально
сконфигуренные qemu-образы на LVM-снапшотах.

Теперь я решил подойти к вопросу серьезнее, взять общепринятые инструменты
и избавиться от костылей.

#####План действий
Возвращаясь к исходной задаче - что же нам нужно для тестирования деплоя с нуля?

1. Базовый образ уже установленной системы
2. Инструмент для создания виртуалки из базового образа с назначением
   нужных сетевых настроек и хостнейма.
3. Скрипт для CI, который будет ресетить виртуалки, запускать на них деплой,
   и проверять корректность результата.

#####Пункт 1
Для реализации первого пункта я сначала взял [Veewee](https://github.com/jedi4ever/veewee), но потом заменил его на [Packer](http://packer.io), который показался
мне заметно более удобным и лишенным костылей Veewee.
Оба эти инструмента берут установочный образ нужного нам дистрибутива,
в моем случае Debian Wheezy, и по описанию создают образ с установленной системой.
Для Debian используется preseed и набор bash-скриптов.

#####Пункт 2
Для реализации второго пункта я взял [Vagrant](http://vagrantup.com).
К сожалению, из коробки Vagrant не поддерживает использование qemu-kvm
в качестве гипервизора, поэтому пришлось использовать также
плагин [vagrant-libvirt](https://github.com/pradels/vagrant-libvirt).
Для конвертации в образ для Vagrant у Packerа есть готовый преобразователь,
но с qemu-kvm он тоже пока не работает, так что образ я собираю по
[этой инструкции](https://github.com/pradels/vagrant-libvirt/tree/master/example_box).
Хочется отметить, что от Vagrant мне нужно только создание-уничтожение виртуалок
и простейшее начальное конфигурирование - настройка сети и хостнейма. Provisioning
с использованием Vagrant и Ansible сейчас для моего случая делать невозможно -
Vagrant генерирует описания групп и хостов для каждой виртуалки отдельно,
а для корректной работы моих playbookов нужно, чтобы хосты знали друг о друге.

#####Пункт 3
Третий пункт - единственный "костыльный", поскольку предполагает написание
скрипта для CI (в моем случае - CruiseControl.rb). Скипт простой, основная
его задача - корректно выставить переменные окружения, отресетить виртуалки, а затем
выполнить последовательно 3 playbookа для определенно группы хостов, проверяя
коды возврата Ansible.

#####Итог
В итоге, я получил ровно то, что и хотел - на каждый коммит в репозиторий с плейбуками
запускается полное развертывание всего окружения на голые операционки. Затем
все нужные компоненты приводятся в требуемое состояние - собираются кластеры,
настраивается репликация - и проверяется запуск всех сервисов и корректность их
состояния после старта. В будущем я планирую добавить тесты, ломающие систему
и проверяющий отказоустойчивость, но это требует больших трудозатрат от наших
разработчиков, которые и так достаточно нагружены.
