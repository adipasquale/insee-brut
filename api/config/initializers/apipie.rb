Apipie.configure do |config|
  config.app_name = "Insee Brut API"
  config.translate = false
  config.default_locale = nil
  config.api_base_url = "/api/v1"
  config.doc_base_url = "/api/docs"
  config.api_controllers_matcher = "#{Rails.root}/app/controllers/api/**/*.rb"
end
