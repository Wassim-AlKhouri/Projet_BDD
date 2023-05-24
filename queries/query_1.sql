SELECT DISTINCT m.medicamentNomCommercial, m.conditionnement
FROM Medicament m
WHERE m.DCI = '{placeholder1}'
ORDER BY m.medicamentNomCommercial ASC, m.conditionnement ASC;