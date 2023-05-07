SELECT med.medicamentNomCommercial
FROM Medicament med
JOIN DossierPatient d ON d.medicamentNomCommercial=med.medicamentNomCommercial
JOIN Patient p ON P.NISS=d.NISS
WHERE p.DateNaissance > {placeholder} AND p.DateNaissance < {placeholder} + 10 
GROUP BY med.medicamentNomCommercial
ORDER BY COUNT(*) DESC
LIMIT 1 

/*
Pour chaque décennie entre 1950 et 2020,(1950−59,1960−69,...),
le médicament le plus consommé 
par des patients nés durant cette décennie
*/
