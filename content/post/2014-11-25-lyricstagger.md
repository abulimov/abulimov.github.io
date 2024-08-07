---
Title: Lyrics Tagger
Date: 2014-11-25
Slug: lyricstagger
Url: it/lyricstagger
Tags: [Python, Программирование]
Categories: [IT, Russian]
Build:
  List: local
---

## Предыстория

Я езжу на работу в общественном транспорте, и слушаю там музыку
со смартфона. Достаточно часто хотелось почитать тексты прослушиваемых
в данный момент песен, но искать их в интернете было не слишком удобно,
да и вообще интернета до недавнего времени в метро не было.

Решение выглядит очевидным - надо встроить тексты песен в сами музыкальные файлы.
Благо, основные форматы это позволяют.
Музыку я храню во [FLAC](https://ru.wikipedia.org/wiki/FLAC), а на смартфон
закидываю в [Ogg Vorbis](https://ru.wikipedia.org/wiki/Vorbis).

Раз есть такая задача - значит можно ее решить с использованием программирования.
Быстрый поиск чего-то подходящего для моих целей ничего не дал, хотя многие плееры
умеют качать тексты песен по запросу.

Поскольку задача не показалась мне сложной, и простая консольная утилита полностью
покрыла бы мои потребности, я решил такую утилиту написать сам.

Выбрал я для реализации, конечно, Python. Все нужные библиотеки там уже были,
а именно:

* [mutagen](https://pypi.python.org/pypi/mutagen) для работы с музыкальными файлами;
* [requests](https://pypi.python.org/pypi/requests) для получения нужных HTML-страниц;
* [beautifulsoup4](https://pypi.python.org/pypi/beautifulsoup4) для разбора HTML;
* [docopt](https://pypi.python.org/pypi/docopt) для удобного написания консольных утилит;
* [mock](https://pypi.python.org/pypi/mock) для тестов.

В итоге получилась вполне компактная программа, покрытая тестами, умеющая качать
тексты песен с [lyrics.wikia.com](http://lyrics.wikia.com/) и записывать в теги
файлов в формате FLAC, Ogg, и MP3 (экспериментально, я MP3 практически на использую).
Модули для поддержки конкретных сайтов с текстами сделаны подключаемыми,
так что можно добавить скачивание с любого другого сайта, не меняя саму программу.

Результатами моих трудов может воспользоваться любой желающий,
[код размещен на Github](https://github.com/abulimov/lyricstagger) под
лицензией [MIT](http://opensource.org/licenses/MIT).
Поддерживается Python версий 2.7, 3.2, 3.3, 3.4 и PyPy.

## Установка

Для установки достаточно выполнить следующую команду:

    ::bash
    pip install 'git+https://github.com/abulimov/lyricstagger#egg=lyricstagger'

## Примеры использования

Вывести список всех музыкальных файлов без встроенных текстов в директории ~/Music/

    ::bash
    user@machine:~$ lyricstagger report ~/Music
    No lyrics in file '/home/user/Music/Some Artist/01 - Some Track.ogg'
    No lyrics in file '/home/user/Music/Some Artist/02 - Other Track.ogg'

Скачать тесты и записать их в теги музыкальных файлов в директории ~/Music/

    ::bash
    user@machine:~$ lyricstagger tag ~/Music

Удалить все теги с текстами из всех музыкальных файлов в ~/Music/

    ::bash
    user@machine:~$ lyricstagger remove ~/Music

## Итоги

Если вы встретились с подобной задачей - попробуйте [lyricstagger](https://github.com/abulimov/lyricstagger),
а если решили эту задачу более простым и удобным способом - напишите мне об этом.
Я уже натравил свою чудо-утилиту на всю музыкальную коллекцию, она записала все
найденные тексты в файлы, так что теперь я запускаю ее только когда покупаю новый
альбом на [Bandcamp](http://bandcamp.com), [CDBaby](http://cdbaby.com) или [Qobuz](http://qobuz.com).
