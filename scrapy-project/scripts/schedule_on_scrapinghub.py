# don't forget to pip3 install scrapinghub before, as it's not in the requirements
# you also have to set the SH_APIKEY environment variable

# this script is setup to run daily as a cron job on a DO droplet.
# just to avoid paying for scrapinghub schedule feature
# which is not very nice sorry :/

from scrapinghub import ScrapinghubClient

client = ScrapinghubClient()
project = client.get_project(362041)
job = project.jobs.run('insee')
print("started scraping job %s" % job.key)
