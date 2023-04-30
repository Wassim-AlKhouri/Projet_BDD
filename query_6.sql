SELECT DISTINCT
m.INAMI, m.Nom,
FROM Medecin m
JOIN Traitement t ON m.INAMI = t.INAMImed
JOIN Medicament med ON t.DCI = med.DCI
JOIN DossierPathologie dp ON t.NISS = dp.NISS
JOIN Pathologie path ON dp.NomP = path.Nom
WHERE m.NomSA <> path.NomSA;

/*
La liste des médecins ayant prescrit des médicaments 
ne relevant pas de leur spécialité
*/