SELECT p.nom
FROM Patient p
JOIN Traitement t ON p.NISS = t.NISS
JOIN Medicament m ON m.DCI = t.DCI 
WHERE m.DCI = {placeholder} 
AND (t.Date_de_debut + t.Duree) < CURDATE() 

/*
Tous les  patients ayant été traités par un médicament (sous sa DCI) 
à une date antérieure mais qui ne le sont plus,
pour vérifier qu’un patient suive bien un traitement chronique
*/
