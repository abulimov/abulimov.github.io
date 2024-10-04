---
Title: Все для HAProxy в Atom
Date: 2016-04-08
Tags: [Golang, Программирование, Atom, HAProxy]
Slug: atom-HAProxy
Url: it/atom-HAProxy
Categories: [IT, Russian]
Build:
  List: local
---

Появилась у меня на работе задачка - взять 3 относительно разных конфига
HAProxy, ответвившихся когда-то от общего предка, и обратно унифицировать их
в один.

Конфиги хорошие, большие - 800 строк каждый.

Приступил я к этой задаче, и сразу оступил - потому что в [Atom](http://atom.io),
которым я пользуюсь для редактирования всего, не было подсветки
синтаксиса конфигов HAProxy.

Ну у нас же тут OpenSource, так что тут же был нагуглен архив с
[HAProxy.tmbundle](https://github.com/williamsjj/HAProxy.tmbundle), который
владелец почему-то удалил. Бандлы TextMate можно конвертировать в плагины
Atom "из коробки", так что именно это я и сделал, и поэтому очень быстро
получил какую-никакую подсветку конфигов.

Довольный, я продолжил рефакторинг этих конфигов, и тут же выяснил, что
подсветка довольно неполная. Перспектива набивать недостающие ключевые слова руками
меня совсем не прельщала, поэтому я быстро набросал примитивнейший
[скрипт на питоне](https://github.com/abulimov/atom-language-HAProxy/blob/master/generate.py),
который парсит официальную документацию HAProxy и выдергивает оттуда ключевые слова,
заполняя шаблон cson-файла с описанием подсветки.

Немного regexp-магии, и подсветка синтаксиса наконец стала меня удовлетворять,
так что я снова вернулся к рефакторингу.

Во время этого увлекательнейшего процесса в голову пришла мысль - насколько же
тут был бы уместен статический анализ, проще говоря - linter. Конечно,
сам HAProxy умеет проверять конфиг, и даже выводит предупреждения на некоторые
вещи, но

* это требует запуска самого HAProxy;
* это не интегрировано в редактор;
* он не показывает повторяющиеся правила;
* он не показывает так называемый deadcode - неиспользуемые части конфига.

Поскольку формат конфигов у HAProxy достаточно простой, а я уже был раззадорен
парсингом документации, пришла идея сделать простенький linter для конфигов HAProxy.

Выбор пал снова на [Go](http://golang.org), поскольку linter должен быть быстрым и надежным.

Конечно, первое, чему я научил свой linter - определение неиспользуемых частей конфига,
поскольку остальное можно было проверить с помощью самого HAProxy.

Как только это заработало, я начал делать плагин для Atom, который бы использовал
вывод моего linterа и отмечал плохие строчки.

Тут я конечно относительно долго тупил, поскольку на JS/CoffeeScript ничего не писал,
но в итоге за первые полдня работы был готов и прототип linter, и плагин для Atom,
так что оставшиеся полдня я рефакторил конфиги.

В процессе я добавлял правила, которые показывали бы те моменты, на которые я
натыкался в процессе рефакторинга, в результате чего на момент
написания этой статьи мой linter умеет сам находить следующие проблемы:

* использованные но не объявленные бекенды;
* объявленные но не используемые бекенды;
* использованные но не объявленные acl;
* объявленные но используемые acl;
* правила, написанные не в том порядке в котором они будут применены;
* дублирование строк конфига;
* наличие deprecated ключевых слов.

Более того, если HAProxy все-таки установлен локально,
linter запускает его в виде `HAProxy -c -f filename`, и парсит его выхлоп.

В этом случае мы не запускаем те из проверок, которые реализованы в самом HAProxy,
например на наличие deprecated ключевых слов. Конечно, эта опция отключаемая.

При этом linter проще простого интегрировать с любым редактором -
у него есть режим вывода всех найденных проблем в JSON.

В общем, конфиг проверяется достаточно досконально, в Atom все изумительно
подсвечивается, так что результатом я более чем доволен и спокойно закончил
рефакторинг тех гигантских конфигов.

Ну а все плоды моих трудов доступны под [лицензией MIT](http://opensource.org/licenses/MIT)
на Github:

* Подсветка синтаксиса конфигов HAProxy в Atom - [atom-language-HAProxy](https://github.com/abulimov/atom-language-HAProxy)
([страничка плагина в Atom](https://atom.io/packages/language-HAProxy))
* Плагин для интеграции HAProxy-lint в Atom - [atom-linter-HAProxy](https://github.com/abulimov/atom-linter-HAProxy)
([страничка плагина в Atom](https://atom.io/packages/linter-HAProxy))
* Сам HAProxy-lint - [HAProxy-lint](https://github.com/abulimov/HAProxy-lint)

P.S. Заодно я научился делать релизы бинарников на Github с помощью
[TravisCI](https://travis-ci.org) - это оказалось очень легко и удобно.