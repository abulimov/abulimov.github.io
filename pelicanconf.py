#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Alexander Bulimov'
ABOUT_ME = 'Меня зовут Александр Викторович Булимов, я сисадмин из Москвы, \
работаю с Linux с 2010 года.\
\
<br>\
<br>\
Практикую методологию DevOps. \
Использую для управления серверами \
<a href=http://www.ansible.com/>Ansible</a>, до этого \
использовал <a href=http://www.opscode.com/chef/>Chef</a>. \
Люблю программировать, автор нескольких модулей к Ansible.\
'
SITENAME = 'Александр Булимов - записки сисадмина.'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Europe/Moscow'

DEFAULT_LANG = 'ru'

PLUGINS = ["related_posts"]

THEME = 'pelican-bootstrap3'
BOOTSTRAP_THEME = 'slate'

SLUGIFY_SOURCE = 'title'
ARTICLE_URL = '{category}/{slug}/'
ARTICLE_SAVE_AS = '{category}/{slug}/index.html'
SUMMARY_MAX_LENGTH = 70
CATEGORIES_URL = 'categories/'
CATEGORIES_SAVE_AS = 'categories/index.html'
TAGS_URL = 'tags/'
TAGS_SAVE_AS = 'tags/index.html'
ARCHIVES_SAVE_AS = 'archive/index.html'
ARCHIVES_URL = 'archive/'

FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# pelican-bootstrap3 settings
DISPLAY_ARTICLE_INFO_ON_INDEX = True
DISPLAY_PAGES_ON_MENU = True
DISPLAY_CATEGORIES_ON_MENU = False
CC_LICENSE = "CC-BY-SA"
CUSTOM_CSS = 'static/custom.css'

# Tell Pelican to add 'custom/custom.css' to the output dir
STATIC_PATHS = ['extra/custom.css', 'extra/CNAME']

# Tell Pelican to change the path to 'static/custom.css' in the output dir
EXTRA_PATH_METADATA = {
    'extra/custom.css': {'path': 'static/custom.css'},
    'extra/CNAME': {'path': 'CNAME'},
    }


# Blogroll
LINKS = (
    ('Pelican', 'http://getpelican.com/'),
    ('Python.org', 'http://python.org/'),
)

# Social widget
SOCIAL = (
    ('GitHub', 'https://github.com/abulimov'),
    ('Facebook', 'https://www.facebook.com/profile.php?id=1505350810'),
    ('Google+', 'https://plus.google.com/102209846851870884693/about'),
    ('LinkedIn', 'http://ru.linkedin.com/pub/александр-булимов/7b/692/a92/'),
    ('Habrahabr', 'http://habrahabr.ru/users/lazywolf/'),
    ('VK', 'http://vk.com/a_v_bulimov'),
    ('RSS', '/feeds/all.rss.xml'),
)


DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True
