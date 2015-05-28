Title: Переписал скрипты на Ruby для Sensu
Date: 2014-09-04
Tags: Ruby, Sensu, Monitoring
Category: IT
Slug: Переписал-скрипты-на-ruby-для-sensu

Поскольку я перевел мониторинг с Zabbix на Sensu, пришлось переписать
свои [скрипты](/it/Низкоуровневое-обнаружение-в-zabbix-ищем-диски-в-контроллере-от-3ware) проверки состояния жестких дисков в raid-контроллерах от 3ware и
HP SmartArray для использования в Sensu. Ну а раз все равно переписывать - то
писать я решил на Ruby, чтобы можно было без проблем
заслать в [sensu-community-plugins](https://github.com/sensu/sensu-community-plugins)

Скрипты весьма просты, так что проблем при переписывании никаких не было.

Если кому надо - все уже отдано сообществу, теперь Sensu может мониторить
состояние дисков [в контроллерах от 3ware](https://github.com/sensu/sensu-community-plugins/blob/master/plugins/raid/check-3ware-status.rb)
и [HP SmartArray](https://github.com/sensu/sensu-community-plugins/blob/master/plugins/raid/check-smartarray-status.rb).

Ну и на закуску - мониторим [статус Riak Ring](https://github.com/sensu/sensu-community-plugins/blob/master/plugins/riak/check-riak-ringready.rb).
