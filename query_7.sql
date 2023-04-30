SELECT med.NomC
FROM Medicament med
JOIN Traitement t ON t.DCI = med.DCI
JOIN Patient p ON P.NISS=t.NISS
WHERE p.DateNaissance > {placeholder} AND p.DateNaissance < {placeholder} + 10 
GROUP BY med.NomC
ORDER BY COUNT(*) DESC
LIMIT 1 

/*
Pour chaque décennie entre 1950 et 2020,(1950−59,1960−69,...),
le médicament le plus consommé 
par des patients nés durant cette décennie
*/
