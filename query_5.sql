SELECT DISTINCT p.nom, p.prenom
FROM Patient p
JOIN DossierPatient d ON d.NISS = p.NISS
WHERE d.DCI = {placeholder1}
AND (d.datePrescription + d.dureeTraitement) < CURDATE()