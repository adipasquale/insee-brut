class Api::V1::InseeDocumentsController < ApplicationController

  before_action :set_insee_document, only: [:show, :edit, :update, :destroy]

  # skip_before_action :verify_authenticity_token, if: Proc.new { |c| c.request.format == 'application/json' }

  def index
    @insee_documents = InseeDocument.all.to_a.first(30)
    render json: @insee_documents
  end

  def show
    render json: @insee_document
  end

  # def create
  #   @insee_document = InseeDocument.new(insee_document_params)

  #   respond_to do |format|
  #     if @insee_document.save
  #       format.json { render json: @insee_document }
  #     else
  #       format.json { render json: @insee_document.errors, status: :unprocessable_entity }
  #     end
  #   end
  # end

  # def update
  #   respond_to do |format|
  #     if @insee_document.update(insee_document_params)
  #       format.json { head :no_content }
  #     else
  #       format.json { render json: @insee_document.errors, status: :unprocessable_entity }
  #     end
  #   end
  # end

  # def destroy
  #   @insee_document.destroy
  #   respond_to do |format|
  #     format.json { head :no_content }
  #   end
  # end

  private
    # Use callbacks to share common setup or constraints between actions.
    def set_insee_document
      @insee_document = InseeDocument.find(params[:id])
    end

    # Never trust parameters from the scary internet, only allow the white list through.
  #   def insee_document_params
  #     content = params.require(:insee_document).fetch(:content, nil).try(:permit!)
  #     params.require(:insee_document).permit(:type, :name, :description, :is_scan, :content).merge(content: content)
  # end
end
