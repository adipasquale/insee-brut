# -*- coding: utf-8 -*-
import scrapy
import logging
import re
import json
import urllib
from insee_crawler.items import Statistiques


class InseeSpider(scrapy.Spider):
    name = 'insee'
    allowed_domains = ['insee.fr']
    current_page = None

    def __init__(self, pages_limit=None, only_id=None, *args, **kwargs):
        self.pages_limit = int(pages_limit) if pages_limit is not None else None
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
            query["filters"].append({"field": "id", "values": [self.only_id]})
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

    def parse_search_results(self, response):
        res = json.loads(response.text)
        for document in res["documents"]:
            if document.get("type") == "statistiques":
                item = Statistiques(
                    insee_id = document["id"],
                    titre = document["titre"],
                    code = document.get("code"),
                    insee_type = document["type"],
                    categorie_id = document.get("categorie", {}).get("id"),
                    categorie_libelle = document.get("categorie", {}).get("libelleFr"),
                    type_produit = document.get("typeProduit"),
                    sous_titre = document["sousTitre"],
                    # auteur = document["auteur"],
                    chapo = document["chapo"],
                    numero = document["numero"],
                    collection = document["collection"],
                    date_diffusion = document["dateDiffusion"],
                    libelle_geographique = document["libelleGeographique"]
                )
                item["url"] = "https://insee.fr/fr/statistiques/%s" % item["insee_id"]
                request = scrapy.Request(
                    item["url"],
                    callback=self.parse_statistiques
                )
                request.meta["item"] = item
                yield(request)
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

        yield(item)