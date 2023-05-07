SELECT DISTINCT p.nom, p.prenom
FROM Patient p
JOIN DossierPatient d ON d.NISS = p.NISS
WHERE d.DCI = {placeholder}
AND (d.datePrescription + d.dureeTraitement) < CURDATE() 

/*
Tous les  patients ayant été traités par un médicament (sous sa DCI) 
à une date antérieure mais qui ne le sont plus,
pour vérifier qu’un patient suive bien un traitement chronique
*/
