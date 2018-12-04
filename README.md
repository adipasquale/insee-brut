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

There is a second API endpoint for 'series' types of data :

```
curl 'https://insee.fr/fr/statistiques/series/ajax/consultation' \
-H 'Accept-Language: fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3' --compressed \
-H 'content-type: application/json; charset=utf-8' \
--data '{"q":"*:*","start":0,"rows":10,"facetsField":[],"filters":[{"field":"bdm_idFamille","values":["103212792"]}],"sortFields":[{"field":"dateDiffusion","order":"desc"},{"field":"bdm_idbankSerie","order":"asc"}]}' \
| jq '.documents | .idBank'
```

you can also perform tests with the small bash script in `/scrapy-project/scripts/test_insee_api.sh`


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
