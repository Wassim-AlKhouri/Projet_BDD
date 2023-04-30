SELECT DISTINCT m.NomC
FROM medicament m
WHERE m.DCI = 'DCI du médicament recherché'
ORDER BY m.NomC ASC, m.Conditionnement ASC;