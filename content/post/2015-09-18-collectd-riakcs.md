---
Title: Плагин к collectd для сбора метрик Riak CS
Date: 2015-09-17
Tags: [Python, Riak CS, collectd, Программирование, Monitoring]
Slug: collectd-riakcs
Url: it/collectd-riakcs
Categories: [IT, Russian]
Build:
  List: local
---

На днях наконец-то дошли руки до модернизации той части мониторинга, которая
отвечает за сбор метрик, и набивший оскомину [Munin](http://munin-monitoring.org) был
окончательно заменен на [Graphite](https://graphite.readthedocs.org/en/latest/) + [CollectD](http://collectd.org).
Теперь воцарилась идиллия - Icinga2 складывает метрики из perfdata в Graphite,
и CollectD отправляет все метрики туда же.

Хочется отдельно отметить, что несмотря на то, что изначально CollectD мне
не очень понравился (кому может сейчас понравиться Apache-подобный конфиг?), при
дальнейшем изучении я был приятно поражен богатством возможностей этого
продукта и крайне бережным его отношением к ресурсам наблюдаемой системы.

Так вот, в процессе переезда с Munin я столкнулся с задачей сбора в CollectD
метрик с замечательной реализации приватного
[S3](https://ru.wikipedia.org/wiki/Amazon_S3)-совместимого хранилища -
[Riak CS](http://docs.basho.com/riakcs/latest).

К слову сказать, с Riak я работаю уже не первый год, и всегда был очень доволен
этим решением, и Riak CS также оправдал все ожидания - он удобный в настройке
и эксплуатации (начиная с версии 2.0 появился даже удобный конфиг - раньше
конфиг был на Erlang), быстрый, надежный, отказоустойчивый, и очень просто масштабируется.
Так что если выбираете хранилище для файлов, доступ к которому нужен по HTTP и
библиотеки для работы с которым есть для любого языка - Riak CS это отличный выбор,
тем более можно при желании смигрировать на любое S3-совместимое хранилище - на
[Ceph](http://ceph.com), например.

Сам Riak CS построен как надстройка над Riak, для которого в официальной
документации [есть пример конфига для CollectD](http://docs.basho.com/riak/1.4.8/ops/running/monitoring/collectd/).

К сожалению, для Riak CS такой фокус с плагином `curl_json` не пройдет - для
доступа к статистике HTTP-запрос должен быть подписан по всем правилам
авторизации S3, поэтому пришлось писать свой плагин, благо CollectD
[предоставляет](https://collectd.org/documentation/manpages/collectd-python.5.shtml#writing_your_own_plugins)
очень простой интерфейс для написания плагинов на Python, а в Python есть
шикарная библиотека [requests](https://www.python-requests.org/), к которой есть удобный
модуль для работы с S3 - [requests-aws](https://github.com/tax/python-requests-aws).

Для написания простейшего плагина к CollectD надо реализовать и
зарегистрировать всего одну функцию - read. То есть вот так выгладит минимальный
плагин к CollectD:

*Пример из официальной документации:*
```Python
import collectd

def read(data=None):
    """collectt and dispatch some data"""
    vl = collectd.Values(type='gauge')
    vl.plugin='python.spam'
    vl.dispatch(values=[random.random() * 100])

collectd.register_read(read)
```

Мне, конечно, пришлось написать немного больше кода, но поскольку сам Riak CS
очень помогает c метриками - он отдает всю нужную информацию, включая
95й и 99й перцентили задержек различных операций, в
[в обычном JSON](http://docs.basho.com/riakcs/latest/cookbooks/Monitoring-and-Metrics/),
это действительно *немного* больше кода.

Плагин получился крошечным - меньше 100 строк кода - и
очень простым.

Код плагина к CollectD для снятия метрик с Riak CS трационно опубликован под
свободной лицензией [MIT](https://opensource.org/licenses/MIT)
на Github - [`collectd-riakcs`](https://github.com/abulimov/collectd-riakcs),
а сам плагин подготовлен к удобной [установке через pip](https://github.com/abulimov/collectd-riakcs#setup).
