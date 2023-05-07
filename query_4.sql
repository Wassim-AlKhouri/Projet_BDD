SELECT DISTINCT p.nom, p.prenom
FROM Patient p
JOIN DossierPatient d ON d.NISS = p.NISS
WHERE d.medicamentNomCommercial = {placeholder1}
AND d.datePrescription >= {placeholder2}

/*
Tous les utilisateurs ayant consommé un médicament spécifique
(sous son nom commercial) après une date donnée,
par exemple en cas de rappel de produit pour lot contaminé
*/
