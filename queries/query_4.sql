SELECT DISTINCT p.nom, p.prenom
FROM Patient p
JOIN DossierPatient d ON d.NISS = p.NISS
WHERE d.medicamentNomCommercial = '{placeholder1}'
AND d.datePrescription >= '{placeholder2}'