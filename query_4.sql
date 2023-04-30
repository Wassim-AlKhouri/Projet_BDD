SELECT DISTINCT p.nom
FROM patient p
JOIN traitement t ON t.NISS = p.NISS
JOIN medicament m ON m.DCI = t.DCI
WHERE m.NomC = 'Nom du médicament recherché'
AND t.Date_de_debut >= 'Date de début recherchée'

/*
Tous les utilisateurs ayant consommé un médicament spécifique
(sous son nom commercial) après une date donnée,
par exemple en cas de rappel de produit pour lot contaminé
*/