module Ruhoh::Resources::Graphs
  class Collection
    include Ruhoh::Base::Collectable

    def url_endpoint
      "/assets/graphs"
    end
  end
end
