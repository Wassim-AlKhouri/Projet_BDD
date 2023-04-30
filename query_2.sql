SELECT DISTINCT p.nom
FROM pathologie p
JOIN systeme_anatomique s ON p.NomSA = s.Nom
WHERE s.nom = {placeholder}
GROUP BY p.nom
HAVING COUNT(DISTINCT Systeme_anatomique) = 1;

/*
La liste des pathologies qui peuvent être prise en charge 
par un seul type de spécialistes
*/
