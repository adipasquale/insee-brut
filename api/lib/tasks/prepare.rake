namespace :prepare do
  task :db => :environment do
    # this task is ran daily on the prod server using a sudo cron
    # 0 4 * * * dokku run api rake prepare:db
    PrepareDbJob.perform_now
  end
end
