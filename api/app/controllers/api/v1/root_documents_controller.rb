class Api::V1::RootDocumentsController < ApplicationController

  def_param_group :root_document do
    property :id_insee, :number, desc: "The ID on the insee.fr site"
    property :auteur, String, desc: 'The author(s) name(s)'
    property :chapo, String, desc: 'A short summary of the contents of the document. Can be up to 5 sentences long.'
    property :collection, String, desc: "A collection name, internal to the Insee. Ex : Insee Première"
    property :collection_id, :number, desc: "This collection's ID for Insee"
    property :collection_url, String, desc: "This collection's URL on insee.fr"
    property :custom, Hash, desc: "Infos added by the system, not original ones"
    property :dateDiffusion, :number, desc: "The publishing date with a weird timestamp format"
    property :dateIndexation, :number, desc: "The indexing date with a weird timestamp format"
    property :embargo, :number, desc: "A date with the same weird timestamp format, but no idea what it means"
    property :famille, Hash, desc: "The family is a hierarchical information."
    property :libelleGeographique, String, desc: "Describes what area is concerned by the document. Ex: France"
    property :numero, String, desc: "A number (but as a string). Not filled all the time. Ex: '1726'"
    property :pdf_url, String, desc: "The downloadable PDF URL on Insee.fr, when available."
    property :themes, Hash, desc: "Another type of hierarchical information. Ex: 'Couples – Familles – Ménages'"
    property :titre, String, desc: "The title of the document."
  end

  api :GET, '/root_documents', 'lists root documents'
  param :page, :number, desc: "the requested page number. should be a positive integer. defaults to 1."
  param :count, :number, desc: "the number of items to return per page. should be a positive integer. defaults to 50."
  param :include_html, String, desc: "include the HTML in the contenu_html key in the response. By default it's false, to avoid slow and heavy responses. Considered true when '1' or 'true'"
  returns array_of: :root_document, desc: "all root documents"
  def index
    count = index_params[:count]&.to_i || 50
    page = index_params[:page]&.to_i || 1
    include_html = ["true", "1"].include?(index_params[:include_html])
    operations = [
      (include_html ? nil : {"$project": {"contenu_html": 0}}),
      {"$sort": {dateDiffusion: -1}},
      {"$skip": (page - 1) * count},
      {"$limit": count}
    ].compact
    @insee_documents = RootDocument.collection.aggregate(operations)
    render json: @insee_documents
  end

  api :GET, '/root_documents/:id', 'gets a single root document'
  param :id, :number, required: true, desc: "The Insee ID for the document (and not the MongoDB ObjectId)"
  returns :root_document
  def show
    @insee_document = RootDocument.find_by({id_insee: params[:id].to_i})
    render json: @insee_document
  end

  private

    def index_params
      params.permit(:count, :page, :include_html)
    end

end
