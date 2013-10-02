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
        g.y_axis_label = dataset['y_axis_label'] if dataset['y_axis_label']
        g.x_axis_label = dataset['x_axis_label'] if dataset['x_axis_label']
        g.labels = dataset['labels']
        dataset['data'].each do |data|
          g.data(data[0], data[1])
        end
        g.minimum_value = dataset['minimum'] if dataset['minimum']

        return g
      end

      def run
        collection = @ruhoh.collection('graphs')
        unless collection.paths?
          Ruhoh::Friend.say { yellow "#{collection.resource_name.capitalize}: directory not found - skipping." }
        return
        end
        Ruhoh::Friend.say { cyan "#{collection.resource_name.capitalize}: (using gruff and yaml)" }
        FileUtils.mkdir_p collection.compiled_path
        collection.files.values.each do |file|
          filepath = file['realpath']
          name = File.basename(filepath, '.*')
          compiled_file = File.join(collection.compiled_path, "#{name}.png")

          #load yaml
          dataset = YAML.load_file(filepath)

          #write graph
          g = self.class.render_graph(dataset)
          g.write(compiled_file)
          Ruhoh::Friend.say { green "  > #{name}.png" }
        end
      end
    end
  end
end
