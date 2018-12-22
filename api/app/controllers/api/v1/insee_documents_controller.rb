class Api::V1::InseeDocumentsController < ApplicationController

  def index
    count = index_params[:count]&.to_i || 50
    page = index_params[:page]&.to_i || 1
    include_html = ["true", "1"].include?(index_params[:include_html])
    operations = [
      {"$match": {"_scrapy_item_class": "Statistiques"}},
      (include_html ? nil : {"$project": {"contenu_html": 0}}),
      {"$sort": {dateDiffusion: -1}},
      {"$skip": (page - 1) * count},
      {"$limit": count}
    ].compact
    @insee_documents = InseeDocument.collection.aggregate(operations)
    render json: @insee_documents
  end

  def show
    @insee_document = InseeDocument.find_by({id_insee: params[:id].to_i})
    render json: @insee_document
  end

  private

    def index_params
      params.permit(:count, :page, :include_html)
    end

end
