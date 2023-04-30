SELECT DISTINCT m.NomC
FROM medicament m
WHERE m.DCI = {placeholder}
ORDER BY m.NomC ASC, m.Conditionnement ASC;
