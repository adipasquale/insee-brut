# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Statistiques(scrapy.Item):
    url = scrapy.Field()
    insee_id = scrapy.Field()
    titre = scrapy.Field()
    sous_titre = scrapy.Field()
    code = scrapy.Field()
    insee_type = scrapy.Field()
    categorie_id = scrapy.Field()
    categorie_libelle = scrapy.Field()
    type_produit = scrapy.Field()
    auteur = scrapy.Field()
    chapo = scrapy.Field()
    numero = scrapy.Field()
    date_diffusion = scrapy.Field()
    libelle_geographique = scrapy.Field()

    pdf_url = scrapy.Field()
    tableaux_data_url = scrapy.Field()

    collection = scrapy.Field()
    collection_id = scrapy.Field()
    collection_url = scrapy.Field()

    pass
