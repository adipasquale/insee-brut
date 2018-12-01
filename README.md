# INSEE Brut

Mirror site for INSEE data aimed to be exhaustive, faster and easier to browse.

## Local setup

```
mkvirtualenv insee-brut
workon insee-brut
pip3 install -f requirements.txt
```

To start a crawl :

```
cd scrapy-project
scrapy crawl insee
```
