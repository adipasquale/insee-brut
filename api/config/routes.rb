Rails.application.routes.draw do
  root to: redirect('/api/docs')

  apipie

  namespace :api, defaults: { format: :json } do
    namespace :v1 do
      resources :root_documents
    end
  end

end
