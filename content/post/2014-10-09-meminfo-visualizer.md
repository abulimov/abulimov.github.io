---
Title: Разбирался с page-cache в Linux
Date: 2014-10-09
Slug: meminfo-visualizer
Url: it/meminfo-visualizer
Tags: [Kernel, Python, Программирование, Книги]
Categories: [IT, Russian]
Build:
  List: local
---

Читая книгу ["Разработка ядра Linux"](http://www.williamspublishing.com/Books/5-8459-1085-4.html) за авторством Роберта Лава,
я решил поглубже разобраться в том, как работает кэш в Linux,
и набрел на вот [эту](http://habrahabr.ru/company/yandex/blog/231957/)
статью на Хабре от Яндекса.

Сама статья весьма познавательна, особенно видео - рекомендую.
Так вот, в этом видео *Роман Гущин*, с помощью простой утилиты, наглядно показывающей
размер кэша, показывал как работает файловый кэш.

Конечно, мне захотелось в образовательных целях написать такую утилиту для себя,
чтобы можно было поиграться с кэшем и видеть изменения.

Выбрал я для реализации свой любимый Python в связке с Qt(PySide).

Вот весь код:

    :::python

    import sys
    from PySide import QtGui, QtCore


    class MemoryDrawer(QtGui.QWidget):

        def __init__(self):
            super(MemoryDrawer, self).__init__()

            self.initUI()
            self.data = dict()
            self.getData()

        def initUI(self):

            self.setWindowTitle('/proc/meminfo visualizer')
            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(self.onTimer)
            self.timer.start(100)
            self.show()

        def paintEvent(self, e):

            qp = QtGui.QPainter()
            qp.begin(self)
            self.drawRectangles(qp)
            qp.end()

        def drawRectangles(self, qp):

            height = self.geometry().height()
            width = self.geometry().width()
            dataSet = [('MemFree:', 'darkGreen'),
                    ('Active(file):', 'darkMagenta'),
                    ('Inactive(file):', 'darkRed'),
                    ('Cached:', 'darkCyan')]
            offset = 20
            count = len(dataSet)
            sizeX = (width - (count + 1) * offset) // count

            sizeY = height - 2 * offset

            x = offset
            y = offset

            for pos, (data, colorName) in enumerate(dataSet):
                x = (pos + 1) * offset + pos * sizeX
                color = QtGui.QColor(colorName)
                pixmap = self.drawGraph(sizeX, sizeY, data, color)
                qp.drawPixmap(x, y, pixmap)

        def drawGraph(self, width, height, dataKey, color):
            memTotal = self.data['MemTotal:']
            kbPerPixel = height / memTotal

            dataValue = self.data[dataKey]
            drawData = dataValue * kbPerPixel

            pixmap = QtGui.QPixmap(width, height)
            qp = QtGui.QPainter()
            qp.begin(pixmap)
            qp.setBrush(QtGui.QColor(255, 255, 255))
            qp.drawRect(0, 0, width, height)
            qp.setBrush(color)
            qp.drawRect(0, height - drawData, width, height)
            qp.drawText(QtCore.QPoint(5, 20), dataKey)
            qp.drawText(QtCore.QPoint(5, 40), "%s kb" % dataValue)
            qp.end()
            return pixmap

        def getData(self):
            with open('/proc/meminfo') as f:
                for line in f.readlines():
                    if line:
                        splitted = line.split()
                        self.data[splitted[0]] = int(splitted[1])

        def onTimer(self):
            self.getData()
            self.update()


    def main():
        app = QtGui.QApplication(sys.argv)
        drawer = MemoryDrawer()
        drawer.show()
        sys.exit(app.exec_())


    if __name__ == '__main__':
        main()

Актуальная версия визуализатора [лежит](https://github.com/abulimov/utils/blob/master/scripts/meminfo.py) в моем репозитории.

Теперь можно самому повторить эксперимент из видео на новых ядрах,
и посмотреть, что же изменилось.

Предварительно надо создать пару больших файлов, для 8Gb оперативки
нам нужны 1Gb и 8Gb файлы. Создать их можно из /dev/urandom примерно так:

    dd if=/dev/urandom bs=1k count=1048576 of=/path/to/large
    dd if=/dev/urandom bs=1k count=8388608 of=/path/to/large2

А еще надо собрать [vmtouch](https://github.com/hoytech/vmtouch):

    wget https://raw.github.com/hoytech/vmtouch/master/vmtouch.c
    gcc -Wall -O3 -o vmtouch vmtouch.c
    chmod +x ./vmtouch

Ну а теперь повторяем эксперимент из видео. Я использовал ядро Linux 3.13.

Для начала, сбросим кэши:

    echo 3 | sudo tee /proc/sys/vm/drop_caches

Запустим визуализатор:

    python3 meminfo.py

У нас есть два больших файлика - large и large2:

Прочитаем large, чтобы он попал в inactive cache:

    cat large > /dev/null

Прочитаем его еще раз, чтобы он попал в active cache:

    cat large > /dev/null

Теперь можно натравить на него vmtouch:

    vmtouch -m 1g -v large

Выдавим его из кэша:

    vmtouch -m 1g -e large

Снова прочитаем large, чтобы он попал в inactive cache:

    cat large > /dev/null

Теперь прочитаем large2

    cat large2 > /dev/null

и видим, что он вытесняет large из inactive cache.

А теперь сбросим снова кэши, и запихнем large в active cache:

    echo 3 | sudo tee /proc/sys/vm/drop_caches
    cat large > /dev/null
    cat large > /dev/null

И попробуем прочитать large2:

    cat large2 > /dev/null

Теперь мы можем видеть, что large2 не может вытеснить large из active cache,
о чем и говорилось в видео.

А еще видно, как колеблется количество свободной памяти, из-за периодического
характера работы kswapd.

Если посмотреть с помощью vmtouch, какая часть large2 попала в inactive cache,
то мы увидим, что он при чтении вытеснял сам себя.

    vmtouch -m 8g -v large2

Теперь можно удалить large, и увидеть, как освободился active cache, а потом
удалить large2 и увидеть, как освободился inactive cache.

Вот такой вот опыт позволяет увидеть некоторые проблемы в работе с кэшами в актуальных
ядрах Linux. Будет интересно повторить эксперимент на свежих ядрах после улучшений
в области Memory Management.
