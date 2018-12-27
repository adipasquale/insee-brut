class PrepareDbJob < ApplicationJob
  def perform
    db = Mongoid::Clients.default
    db[:root_documents].drop()
    db[:insee_items].aggregate([
      {"$match": {"_scrapy_item_class": "RootDocument"}},
      {"$out": "root_documents"}
    ]).each{}  # you have to iterate it to execute
    fields_to_delete = [
      "_scrapy_item_class", # always RootDocument
      "alaUne", # always false
      "categorie.enfants", # is set in .7% cases, always []
      "categorie.idParent", # is set in .7% cases, always null
      "categorie.libelleEn", # is set in .7% cases, always null
      "categorie.ordre", # is set in .7% cases, always null
      "categorie.sousCategorie", # is set in .7% cases, always []
      "code", # is set in .7%
      "composite", # always false or unset
      "contenu", # always false or unset
      "diffusion", # always true or unset
      "etat", # always {"id": 4} ?
      "famille.active", # always null
      "famille.alaUne", # always null
      "famille.avisParution", # always null
      "famille.avisParution", # always null
      "famille.categorie.enfants", # always []
      "famille.categorie.idParent", # always null
      "famille.categorie.libelleEn", # always null
      "famille.categorie.ordre", # always null
      "famille.categorie.sousCategorie", # always []
      "famille.collection", # always false
      "famille.diffusion", # always null
      "famille.enfants", # always []
      "famille.epsilon", # always null
      "famille.facetteActualiteSSM", # always null
      "famille.facetteCollection", # always null
      "famille.facetteConjoncture", # always null
      "famille.filActualite", # always null
      "famille.gabarit", # always null
      "famille.heureembargo", # always null
      "famille.idMetierDecouvrirCollection", # always null
      "famille.indicateurPrincipal", # always null
      "famille.indicateurSecondaire", # always null
      "famille.lettreInfo", # always null
      "famille.libelleCourt", # always null
      "famille.libelleEn", # always null
      "famille.logo", # always false
      "famille.methodologie", # always null
      "famille.ongletNavTransverse", # always null
      "famille.ordre", # always null
      "famille.presentationEn", # always null
      "famille.presentationFr", # always null
      "famille.prochaineParution", # always null
      "famille.rss", # always null
      "famille.rubrique", # always 'statistiques'
      "famille.sensible", # always null
      "famille.service", # always null
      "famille.source", # always null
      "famille.twitter", # always null
      "famille.typeFormulaire", # always null
      "indexerSeries", # set in .7% to false
      "isProduit", # set in 99.3% to true
      "langue", # set in .7% to 'FR'
      "pedagogique", # set in 99.3% to false
      "quizz", # set in 99.3% to false
      "rubrique", # set to false or 'statistiques'
      "themes.id", # always null
      "themes.idThemeParent", # always null
      "themes.libelleAfficheEn", # always null
      "themes.libelleAfficheFr", # always null
      "themes.libelleCourt", # always null
      "themes.libelleEn", # always null
      "themes.ordre", # always null
      "themes.sousTheme", # always []
      "timeDerniereMiseEnLigne", # always 0
      "traduit", # always false
      "type", # always 'statistiques'
      "verrou", # always false
      "versionHtml", # always false
    ]

    unset_obj = Hash[fields_to_delete.map{|f| [f, 1]}]
    db[:root_documents].update_many({}, {"$unset": unset_obj})

    db[:root_documents].indexes.create_one({"dateDiffusion": -1});
    db[:root_documents].indexes.create_one({"id_insee": 1});
  end
end

