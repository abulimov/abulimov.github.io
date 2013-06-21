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
          g = self.class.render_graph(dataset)
          g.write(compiled_file)
          Ruhoh::Friend.say { green "  > #{name}.png" }
        end
      end
    end
  end
end
