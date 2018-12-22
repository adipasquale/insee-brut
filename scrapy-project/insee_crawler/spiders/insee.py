# -*- coding: utf-8 -*-
import scrapy
import logging
import re
import json
import urllib
from insee_crawler.items import StatistiquesLoader, Statistiques, SerieLoader, Serie

class InseeSpider(scrapy.Spider):
    name = 'insee'
    allowed_domains = ['insee.fr']
    current_page = None

    def __init__(self, pages_limit=None, only_id=None, skip_contenu=False, *args, **kwargs):
        self.pages_limit = int(pages_limit) if pages_limit is not None else None
        self.skip_contenu = skip_contenu
        self.only_id = only_id
        super(InseeSpider, self).__init__(*args, **kwargs)

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

    def series_request(self, insee_id, page=1):
        query = {
            "q": "*:*",
            "start": (page - 1) * 100,
            "rows": 100,
            "facetsField":[],
            "filters": [
                {"field":"bdm_idFamille","values":["%s" % insee_id]}
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
        request.meta["insee_id"] = insee_id
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
                response.meta["insee_id"],
                page=response.meta["page"] + 1)
            )

    def parse_search_results(self, response):
        res = json.loads(response.text)
        for document in res["documents"]:
            loader = StatistiquesLoader(Statistiques())
            document["id_insee"] = document.pop("id")
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
                yield(self.series_request(item["id_insee"]))
                yield(item)
            else:
                yield(item)
        if len(res["documents"]):
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
