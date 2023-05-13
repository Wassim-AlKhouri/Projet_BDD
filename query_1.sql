SELECT DISTINCT m.medicamentNomCommercial
FROM Medicament m
WHERE m.DCI = {placeholder1}
ORDER BY m.medicamentNomCommercial ASC, m.conditionnement ASC;