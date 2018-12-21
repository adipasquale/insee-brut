class InseeDocument
  include Mongoid::Document
  store_in collection: "insee_items"
  include Mongoid::Attributes::Dynamic
end
