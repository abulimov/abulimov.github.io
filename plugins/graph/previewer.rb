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
