from datetime import datetime
import re
from data_page_builder import DataPageBuilder

class RootItemsAugmenter:

    def __init__(self, items):
        self.items = items

    def augment(self):
        for item in self.items:
            item["date_diffusion_lisible"] = datetime.utcfromtimestamp(int(item["dateDiffusion"]/1000)).strftime('%d/%m/%Y')
            item["path"] = DataPageBuilder.path_for_data_page(item)
            if item.get("contenu_html"):
                item["contenu_html"] = re.subn(r"src=\"\/", "src=\"https://insee.fr/", item["contenu_html"])[0]

            categorie = ""
            categorie_color = ""
            if item.get("collection") and (re.match(r'^Insee ', item["collection"]) or item["collection"] == "Informations rapides"):
                categorie = "%s - N°%s" % (item["collection"], item["numero"])
                categorie_color = "orange"
            elif item.get("famille"):
                if item["famille"].get("libelleFr") == "Outils interactifs":
                    categorie = item["famille"]["libelleFr"]
                    categorie_color = "dark-green"
                if item["famille"].get("libelleFr") == "Séries chronologiques":
                    categorie = item["famille"]["libelleFr"]
                    categorie_color = "green"
                elif item["famille"].get("categorie", {}).get("libelleFr") in ["Chiffres-clés", "Chiffres détaillés"]:
                    categorie = item["famille"]["categorie"]["libelleFr"]
                    if categorie == "Chiffres-clés":
                        categorie_color = "blue"
                    else:
                        categorie_color = "dark-blue"
            elif item.get("categorie", {}).get("libelleFr"):
                categorie = item["categorie"]["libelleFr"]
                categorie_color = "green"
            else:
                categorie = item.get("insee_type")
            item["custom"]["categorie"] = categorie
            item["custom"]["categorieCouleur"] = categorie_color

        return self.items