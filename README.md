# INSEE Brut

Mirror site for INSEE data aimed to be exhaustive, faster and easier to browse.

## Overall architecture

The Scrapy spider will run nightly on [ScrapingHub](https://scrapinghub.com/). It should fetch all data from the insee.fr website.

Then, a python build script will recompile Mustache templates using the scraped data and publish it. This will run on [Netlify](https://www.netlify.com/).

## Scraping

## testing INSEE solr API

The INSEE search page uses an AJAX call to un unprotected JSON API that gives us a lot of details.

You can test it in your browser with :

```
curl 'https://insee.fr/fr/solr/consultation?q=*:*' \
-H 'Accept: application/json, text/javascript, */*; q=0.01' \
-H 'Content-Type: application/json; charset=utf-8' \
--data '{"q":"*:*","start":0,"sortFields":[{"field":"dateDiffusion","order":"desc"}],"filters":[{"field":"rubrique","tag":"tagRubrique","values":["statistiques"]},{"field":"diffusion","values":[true]}],"rows":100,"facetsQuery":[]}' \
| jq '.documents[] .titre'
```

It's possible to add a filter with an ID : `{"field":"id","values":[3648291]}`

I'm using [jq](https://stedolan.github.io/jq/) here for parsing the results inline.

### Deploy Scrapy spider to Scrapinghub

The first time, you need the shub dependency

```
pip3 install shub
shub login
```

And then each time you want to deploy :

```
cd scrapy-project
shub deploy 362041
```

## Local setup

```
mkvirtualenv insee-brut
workon insee-brut
pip3 install -r requirements.txt -r requirements-dev.txt
```

To start a crawl :

```
cd scrapy-project
scrapy crawl insee
```
