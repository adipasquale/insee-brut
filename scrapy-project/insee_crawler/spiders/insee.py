# -*- coding: utf-8 -*-
import scrapy
import logging
import re
import json
import urllib
from insee_crawler.items import RootDocumentLoader, RootDocument, SerieLoader, Serie
from insee_crawler.mongo_provider import MongoProvider


class InseeSpider(scrapy.Spider):
    name = 'insee'
    allowed_domains = ['insee.fr']
    current_page = None

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        kwargs['mongo_uri'] = crawler.settings.get("MONGO_URI")
        kwargs['mongo_database'] = crawler.settings.get('MONGO_DATABASE')
        return super(InseeSpider, cls).from_crawler(crawler, *args, **kwargs)

    def __init__(
        self, pages_limit=None, only_id=None, skip_contenu=False,
        only_root_documents=False, force_rescrape=False,
        mongo_uri=None, mongo_database=None,
        *args, **kwargs
    ):
        self.pages_limit = int(pages_limit) if pages_limit is not None else None
        self.skip_contenu = skip_contenu
        self.only_root_documents = only_root_documents
        self.only_id = only_id
        self.force_rescrape = force_rescrape
        self.mongo_provider = MongoProvider(mongo_uri, mongo_database)
        self.last_scraped_item = self.find_last_scraped_item()
        super(InseeSpider, self).__init__(*args, **kwargs)

    def find_last_scraped_item(self):
        collection = self.mongo_provider.get_collection()
        last_items = collection. \
            find({"_scrapy_item_class": "RootDocument"}). \
            sort("dateDiffusion", -1). \
            limit(1)
        return last_items[0] if last_items.count() else None

    def start_requests(self):
        return [
            self.next_page_request()
        ]

    def next_page_request(self):
        if self.current_page is None:
            self.current_page = 0
        else:
            self.current_page += 1

        if self.only_id and self.current_page > 0:
            # do not even try to crawl second page
            return None

        if self.pages_limit is not None and self.current_page >= self.pages_limit:
            return None

        query = {
            "q":"*:*",
            "start": self.current_page * 100,
            "sortFields": [
                {"field":"dateDiffusion","order":"desc"}
            ],
            "filters": [
                {"field": "rubrique", "tag": "tagRubrique", "values": ["statistiques"]},
                {"field": "diffusion", "values": [True]}
            ],
            "rows": 100,
            "facetsQuery":[]
        }
        if self.only_id:
            query["filters"].append({"field": "id_insee", "values": [self.only_id]})
        return scrapy.Request(
            "https://insee.fr/fr/solr/consultation?q=*:*",
            method="POST",
            body=json.dumps(query),
            headers={
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Content-Type': 'application/json; charset=utf-8'
            },
            callback=self.parse_search_results
        )

    def series_request(self, id_insee, page=1):
        query = {
            "q": "*:*",
            "start": (page - 1) * 100,
            "rows": 100,
            "facetsField":[],
            "filters": [
                {"field":"bdm_idFamille","values":["%s" % id_insee]}
            ],
            "sortFields": [
                {"field": "dateDiffusion", "order": "desc"},
                {"field": "bdm_idbankSerie", "order": "asc"}
            ]
        }
        request = scrapy.Request(
            "https://insee.fr/fr/statistiques/series/ajax/consultation",
            method="POST",
            body=json.dumps(query),
            headers={
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Content-Type': 'application/json; charset=utf-8'
            },
            callback=self.parse_series_results
        )
        request.meta["id_insee"] = id_insee
        request.meta["page"] = page
        return request

    def parse_series_results(self, response):
        json_response = json.loads(response.text)
        for document in json_response["documents"]:
            document["id_insee"] = document.pop("id")
            loader = SerieLoader(Serie())
            loader.add_value(None, document)
            serie = loader.load_item()
            yield(serie)
        if len(json_response["documents"]) == 100:
            yield(self.series_request(
                response.meta["id_insee"],
                page=response.meta["page"] + 1)
            )

    def parse_search_results(self, response):
        res = json.loads(response.text)
        last_scraped_item_reached = False
        for document in res["documents"]:
            loader = RootDocumentLoader(RootDocument())
            document["id_insee"] = document.pop("id")
            if self.last_scraped_item and document["id_insee"] == self.last_scraped_item["id_insee"]:
                logging.info("reached last scraped item %s, will stop at the end of this page." % document["id_insee"])
                last_scraped_item_reached = True
                # we don't return here because we're not super confident with the sort order,
                # so this should do a few extra requests but avoid missing too many new itmes
            loader.add_value(None, document)
            loader.add_value("custom", {})
            item = loader.load_item()
            if document.get("type") == "statistiques":
                item["custom"]["insee_url"] = "https://insee.fr/fr/statistiques/%s" % item["id_insee"]
                request = scrapy.Request(
                    item["custom"]["insee_url"],
                    callback=self.parse_statistiques
                )
                request.meta["item"] = item
                yield(request)
            elif item.get("categorie", {}).get("libelleFr") == "Séries chronologiques":
                item["custom"]["insee_url"] = "https://insee.fr/fr/statistiques/series/%s" % item["id_insee"]
                if not self.only_root_documents:
                    yield(self.series_request(item["id_insee"]))
                yield(item)
            else:
                yield(item)
        if len(res["documents"]) and (not last_scraped_item_reached or self.force_rescrape):
            yield(self.next_page_request())

    def parse_statistiques(self, response):
        item = response.meta["item"]
        item["auteur"] = response.css(".auteurs::text").extract_first()

        collection_link = response.css('a[data-i18n="produit.bandeau-bleu.decouvrir-collection"]')
        if collection_link:
            path = collection_link.css("::attr(href)").extract_first()
            match = re.match(r"\/fr\/information\/(\d+)", path)
            if match:
                item["collection_id"] = int(match.groups()[0])
                item["collection_url"] = response.urljoin(path)

        if response.css(".donnees-telechargeables"):
            for download_link in response.css(".donnees-telechargeables a"):
                txt = "".join(download_link.css("*::text").extract())
                url = response.urljoin(download_link.css("::attr(href)").extract_first())
                if "imprimable" in txt:
                    item["pdf_url"] = url
                elif "tableaux" in txt:
                    item["tableaux_data_url"] = url

        if not self.skip_contenu:
            item["contenu_html"] = response.css("#consulter").extract_first()

        yield(item)

