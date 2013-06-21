---
title: "Плагин к Ruhoh для рисования графиков"
date: '2013-06-21'
tags: [ Программирование, IT, Ruby, Ruhoh ]
categories: IT
---

Еще планируя создание статического блога на Hakyll я хотел реализовать рисование
графиков "на лету" из отдельно хранящихся данных. Но с Hakyll не сложилось,
и после долгих поисков я остановился на [Ruhoh](http://ruhoh.com/).

Все нижеописанное относится к **Ruhoh 2.1**

###Цель

Рисовать графики из данных, хранящихся в человеко-читаемом виде.
Нужно мне это было для визуализации своих спортивных тренировок.

###Решение

Конечно, я решил оформить все в виде плагина к Ruhoh, благо возможность такая есть,
да и программировать я люблю. Язык разработки Ruby, поскольку сам Ruhoh написан на Ruby.

Документация конечно не блещет, так что пришлось покопаться всходном коде Ruhoh.

В результате появился плагин, берущий данные из yaml-файлов, и стоящий по ним графики
с помощью [gruff](http://rubygems.org/gems/gruff).

Плагин состоит из 3х файлов:

**collection.rb**

<pre>
module Ruhoh::Resources::Graphs
  class Collection
    include Ruhoh::Base::Collectable

    def url_endpoint
      "/assets/graphs"
    end
  end
end
</pre>

Тут мы кроме url\_endpoint ничего особо и не описывам. Url\_endpoint нужен для указания,
где будут в итоге лежать получившиеся графики

**compiler.rb**

<pre>
require 'gruff'
require 'yaml'
class Ruhoh
  module Compiler
    class Graphs
      def initialize(ruhoh)
        @ruhoh = ruhoh
      end

      def self.render_graph(dataset)

        #create graph
        type = dataset['type'] || 'line'
        size = dataset['size'] || 400
        klass = Gruff.const_get(type.capitalize)
        g = klass.new(size)
        g.title = dataset['title'] || 'Unknown'
        g.theme_pastel()
        g.y_axis_increment = dataset['step'] if dataset['step']
        g.labels = dataset['labels']
        dataset['data'].each do |data|
          g.data(data[0], data[1])
        end
        return g
      end

      def run
        collection = @ruhoh.collection('graphs')
        unless collection.paths?
          Ruhoh::Friend.say { yellow "#{collection.resource_name.capitalize}: directory not found - skipping." }
        return
        end
        Ruhoh::Friend.say { cyan "#{collection.resource_name.capitalize}: (using gruff and yaml)" }
        compiled_path = Ruhoh::Utils.url_to_path(@ruhoh.to_url(collection.url_endpoint), @ruhoh.paths.compiled)
        FileUtils.mkdir_p compiled_path
        collection.files.values.each do |file|
          filepath = file['realpath']
          name = File.basename(filepath, '.*')
          compiled_file = File.join(compiled_path, "#{name}.png")

          #load yaml
          dataset = YAML.load_file(filepath)

          #write graph
          g = self.render_graph(dataset)
          g.write(compiled_file)
          Ruhoh::Friend.say { green "  > #{name}.png" }
        end
      end
    end
  end
end
</pre>

Тут все уже интереснее. В методе *render\_graph* описана сама процедура создания графика,
а в методе run мы обходим все файлы *коллекции*, и из них генерируем этим самым
методом *render\_graph* итоговые картинки, и помещаем куда нужно.

Ну и для того, чтобы в preview-режиме мы тоже могли видеть эти картинки, существует файл

previewer.rb

<pre>
require 'gruff'
require 'yaml'
module Ruhoh::Resources::Graphs
  class Previewer
    def initialize(ruhoh)
      @ruhoh = ruhoh
    end

    def call(env)
      collection = @ruhoh.collection('graphs')
      file_name = File.basename(env["PATH_INFO"], '.*')
      file = collection.find_file("#{file_name}.yml")
      if file then
        file_path = file['realpath']
        dataset = YAML.load_file(file_path)

        g = Ruhoh::Compiler::Graphs.render_graph(dataset)

        #write graph
        blob = g.to_blob(fileformat='PNG')
        [200, {'Content-Type' => 'image/png'}, [blob]]
      else
        [404, {'Content-Type' => 'text/html'}, ["#{file_name} not found"]]
      end
    end
  end
end
</pre>

В нем описывается, как по запрошенному URL отдать сгенерированную "на лету" картинку,
используя метод render\_graph из compiler.rb.

Актуальные версии описанных файлов можно найти в моем [репозитории](https://github.com/abulimov/abulimov.github.io), где хранятся исходники этого блога.
