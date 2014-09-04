---
title: "Открыл для себя плагины к tmux"
date: '2014-09-04'
tags: [ Администреж, IT ]
categories: IT
---
Случилось чудесное - [LOR](http://linux.org.ru) принес мне пользу.
Оттуда я узнал о плагине [tmux-resurrect](https://github.com/tmux-plugins/tmux-resurrect),
а точнее, вообще о существовании плагинов для чудесного мультиплексора терминалов **tmux**.


С помощью имеющихся плагинов можно привести конфигурацию в более понятный вид,
а также заменить свои костыли на костыли, поддерживаемые сообществом.

Я, к примеру:

* сильно сократил конфигурацию, используя
  [tmux-sensible](https://github.com/tmux-plugins/tmux-sensible);
* с помощью [tmux-yank](https://github.com/tmux-plugins/tmux-yank)
  выкинул свои костыли для копирования в буфер обмена;
* смог убрать настройки для vi-образной навигации между панелями
  благодаря [tmux-pain-control](https://github.com/tmux-plugins/tmux-pain-control);
* обрел поиск с помощью [tmux-copycat](https://github.com/tmux-plugins/tmux-copycat);
* теперь могу открывать выделенные файлы либо URL
  с помощью [tmux-open](https://github.com/tmux-plugins/tmux-open);
* наконец, могу сохранять все открытые окна и панели tmux
  с использованием [tmux-resurrect](https://github.com/tmux-plugins/tmux-resurrect);
