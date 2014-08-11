---
title: "Модуль zabbix_maintenance"
date: '2014-08-11'
tags: [ Администреж, IT, Ansible, Python ]
categories: IT
---
Свершилось чудо, и мой [модуль](https://github.com/ansible/ansible/blob/devel/library/monitoring/zabbix_maintenance)
для Ansible, который умеет создавать и удалять периоды "в обслуживании" в Zabbix,
наконец-то [приняли](https://github.com/ansible/ansible/pull/5062) в апстрим.
Это уже третий мой модуль, принятый в апстрим Ansible.

Краткая история:

Модуль этот я запушил еще в 26 ноября 2013 года, но 21 декабря
[cove](https://github.com/cove) написал в комментарии к моему модулю,
что планирует выложить целую [пачку](https://github.com/ansible/ansible/pull/6034)
модулей для взаимодействия с Zabbix из Ansible.
Это отложило принятие моего модуля в апстрим почти на 9 месяцев,
поскольку мы согласовывали интерфейс наших модулей, тестировали и улучшали модули,
выложенные cove, а очередь pull-requestов у Ansible выросла до 300+.

Теперь, когда *zabbix\_maintenance* уже влит в основную ветку, а модули cove готовы к этому,
можно будет практически полностью исключить ручное взаимодействие с инопланетным
интерфейсом Zabbixа.

Свой модуль я использую примерно так:

**rolling-update.yml**
{{=<% %>=}}

<pre>
- hosts: www
  serial: 1
  vars_prompt:
    - name: zabbix_user
      prompt: "Username for Zabbix API"
      default: false
      private: no
    - name: zabbix_password
      prompt: "Password for Zabbix API"
      default: false
      private: yes
  pre_tasks:
    - name: disable server in haproxy
      shell: "/opt/haproxywrap.sh disable application/{{ ansible_hostname }}"
      delegate_to: "{{ item }}"
      with_items: groups["lb"]

    - name: create maintenance for server in zabbix
      delegate_to: 127.0.0.1
      zabbix_maintenance: login_user={{ zabbix_user }}
                          login_password={{ zabbix_password }}
                          server_url=https://zabbix.example.com
                          host_name={{ ansible_hostname }}
                          state=present
                          name="Update of {{ ansible_hostname }}"
                          minutes=30

  # тут у меня проход по всем ролям с выполнением кучи
  # действий, но для примера пусть будет так
  tasks:
    - apt: upgrade=dist update_cache=yes

  post_tasks:
    - name: enable the server in haproxy
      shell: "/opt/haproxywrap.sh enable application/{{ ansible_hostname }}"
      delegate_to: "{{ item }}"
      with_items: groups["lb"]

    - name: remove maintenance for server in zabbix
      delegate_to: 127.0.0.1
      zabbix_maintenance: login_user={{ zabbix_user }}
                          login_password={{ zabbix_password }}
                          server_url=https://zabbix.example.com
                          state=absent
                          name="Update of {{ ansible_hostname }}"
</pre>
<%={{ }}=%>

В этом плейбуке для каждого хоста по очереди выполняются следующие действия:

1. выключаем сервер приложений на балансировщике haproxy, делегируя
действие хостам из группы "lb"

2. создаем период "в обслуживании" на 30 минут для обновляемого хоста

3. обновляем хост

4. включаем его обратно на балансировщике

5. удаляем период "в обслуживании"

P.S. скрипт haproxywrap.sh можно взять [тут](https://github.com/abulimov/utils/blob/master/scripts/haproxywrap.sh)
