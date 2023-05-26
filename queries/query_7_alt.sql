SELECT med.medicamentNomCommercial
FROM Medicament med
JOIN DossierPatient d ON d.medicamentNomCommercial=med.medicamentNomCommercial
JOIN Patient p ON p.NISS=d.NISS
WHERE p.DateNaissance > '{placeholder1}' AND p.DateNaissance < '{placeholder2}' + 10 
GROUP BY med.medicamentNomCommercial
ORDER BY COUNT(*) DESC
LIMIT 1;