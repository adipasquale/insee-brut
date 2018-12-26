Apipie.configure do |config|
  config.app_name = "Insee Brut API"
  config.app_info = <<-EOS
    This API provides programmatic and free access to the Open Data documents scraped from the insee.fr website.

    See https://github.com/adipasquale/insee-brut for more details.
  EOS
  config.translate = false
  config.default_locale = nil
  config.api_base_url = "/api/v1"
  config.doc_base_url = "/api/docs"
  config.api_controllers_matcher = "#{Rails.root}/app/controllers/api/**/*.rb"
end
