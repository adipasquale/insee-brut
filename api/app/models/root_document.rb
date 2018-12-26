class RootDocument
  include Mongoid::Document
  store_in collection: "root_documents"
  include Mongoid::Attributes::Dynamic
end
