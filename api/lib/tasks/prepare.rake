namespace :prepare do
  task :db => :environment do
    PrepareDbJob.perform_now
  end
end
