---
Title: Ansible и serverspec
Date: 2014-05-22
Tags:   [Ansible, serverspec, Мнение]
Categories: [IT, Russian]
Slug: ansible-и-serverspec
Url: it/ansible-и-serverspec
---

Когда я готовил playbook для [своего VPS](/it/Личный-vps), я взял за основу
[Sovereign](https://github.com/al3x/sovereign). В этом репозитории меня
заинтересовал файл **tests.py**, содержащий тесты для результирующего сервера.
У меня сразу же возник вопрос - почему тесты самописные, на голом Python, а
не на каком-нибудь готовом решении. Я решил изучить, что же есть сейчас для
TDD-администрирования. Оказалось, что толком ничего и нет, а то, что
есть - для Ansible не особо нужно.

Для начала, что есть. Тут все скучно, есть [serverspec](http://serverspec.org/),
и [`envassert`](https://pypi.python.org/pypi/envassert). Оба эти инструмента
предоставляют возможность декларативно описать требуемое состояние удаленного
сервера, и проверить его соответствие реальности по ssh.

Вот пример для serverspec с официального сайта:

    :::ruby
    require 'spec_helper'

    describe package('httpd') do
      it { should be_installed }
    end

    describe service('httpd') do
      it { should be_enabled   }
      it { should be_running   }
    end

    describe port(80) do
      it { should be_listening }
    end

    describe file('/etc/httpd/conf/httpd.conf') do
      it { should be_file }
      its(:content) { should match /ServerName www.example.jp/ }
    end

Все чудесно, и для того же Chef это отличный инструмент, поскольку
сам Chef провоцирует писать императивный код на Ruby, который хорошо было бы
проверять простым декларативным описанием.

Но в случае Ansible, наш playbook **уже** содержит декларативное описание
требуемого состояния.

Вот фрагмент роли Nginx для Ansible.

    :::yaml
    - name: Ensure nginx package is installed
      apt: pkg=nginx state=latest

    - name: Ensure nginx service is enabled and started
      service: name=nginx state=started enabled=yes

    - name: Place nginx.conf
      template: src=nginx.conf.j2 dest=/etc/nginx/nginx.conf mode=644
      notify:
        - reload nginx

Как можно заметить, описание Ansible не содержит только проверок портов, зато
позволяет привести систему к описываемому виду, а не только проверить на соответствие.

Таким образом, имеет смысл использовать serverspec с Ansible только для проверки
таких параметров, как слушающие порты, правила iptables, и настройки сетевых
интерфейсов - все остальное Ansible и проверяет, и приводит к нужному состоянию.
Но в боевой системе, или в staging-окружении, эти параметры и так будут проверяться
системой мониторинга, причем на постоянной основе.

Видимо, именно поэтому репозиторий sovereign содержит самописные тесты, которые
проверяют не столько состояние системы, сколько корректность работы
сконфигурированных сервисов. К сожалению, инструмент, который бы облегчил задачу
написания таких тестов, еще не написан, хотя было бы здорово расширить serverspec
для проверки корректности работы HTTP-сервисов, либо imap-сервера, дополнить его
более высокоуровневыми проверками.

Я для себя пока решил, что написание serverspec-тестов для Ansible избыточно
при наличии staging-окружения с работающим мониторингом и фунциональными тестами,
однако инструмент это явно полезный и перспективный.
