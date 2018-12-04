curl 'https://insee.fr/fr/statistiques/series/ajax/consultation' \
-H 'Accept-Language: fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3' --compressed \
-H 'content-type: application/json; charset=utf-8' \
--data '{
  "q": "*:*",
  "start": 0,
  "rows": 10,
  "facetsField": [
  ],
  "filters": [
    {
      "field": "bdm_idFamille",
      "values": [
        "103212792"
      ]
    }
  ],
  "sortFields": [
    {
      "field": "dateDiffusion",
      "order": "desc"
    },
    {
      "field": "bdm_idbankSerie",
      "order": "asc"
    }
  ]
}' \
| jq '.documents[] | .idBank' | head