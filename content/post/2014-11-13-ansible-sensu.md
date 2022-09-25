---
Title: Удобная настройка Sensu с Ansible
Date: 2014-11-13
Slug: ansible-sensu
Url: it/ansible-sensu
Tags: [Ansible, Sensu, Monitoring]
Categories: [IT, Russian]
---

Так как я использую [Sensu](http://sensuapp.org/) для мониторинга,
и [Ansible](http://www.ansible.com/) для управления конфигурациями,
то конечно же я настраиваю Sensu с помощью Ansible.

В этой связке меня смущало только одно - Sensu использует
[JSON](https://ru.wikipedia.org/wiki/JSON) для конфигов,
в то время как Ansible использует [YAML](https://ru.wikipedia.org/wiki/YAML).
Поскольку JSON является подмножеством YAML, и описывать
конфигурации в YAML гораздо проще (никаких проблем с запятыми, скобочками),
хотелось писать в YAML и транслировать в JSON.

Начал я, конечно, с использования шаблонов Ansible:

    :::json
    {
        "client": {
            "address": "{{ ansible_default_ipv4.address }}",
            "name": "{{ ansible_hostname }}",
            "subscriptions": [ "{{ sensu_client_subscriptions|join('", "') }}" ]
        }
    }

Вроде неплохо, но не слишком удобно, и если одним клиентам захочется добавить
что-то, например переменную `some_var`, надо для них делать новый шаблон, или
городить строки такого вида:

    {% if some_var is defined %} "some_var": {{ some_var }}, {% endif %}

В общем, я, не особо включая мозг, решил писать модуль для Ansible.

В процессе написания выплыли все те же проблемы: сложно работать с произвольного
вида структурами, которые позволяют с такой гибкостью использовать Sensu.

То есть для примера с добавлением переменной клиенту, нашему модулю пришлось бы
поддерживать не только обязательные параметры клиента, такие как имя, адрес
и список подписок, но еще и аргумент, в который мы пихали бы остальные данные.
Да еще и структура описания у Sensu в тот момент менялась от версии к версии.

И тут я наткнулся на [pull-request](https://github.com/ansible/ansible/pull/2234),
из которого узнал, что теперь в Ansible можно использовать =
фильтры *to_json* и *to_nice_json*.

А это дает нам возможность делать такие вещи:

    :::yaml
    # task from sensu_client role
    - name: configure sensu client
      copy: content='{{ sensu_client | to_nice_json }}'
            owner=sensu
            dest=/etc/sensu/conf.d/client.json
      notify:
        - restart sensu-client

А описание переменной *sensu_client* где-нибудь в *group_vars* выглядит так:

    :::yaml
    sensu_client:
      client:
        name: "{{ ansible_hostname }}"
        subscriptions:
          - www
          - default
        address: "{{ ansible_default_ipv4.address }}"
        some_var: "{{ sensu_some_var }}"

Эта схема показалась мне достаточно удобной, и на этом я остановился,
так что теперь весь конфиг Sensu, включая проверки, хендлеры и т.д., хранится
у меня в формате YAML в Ansible.
