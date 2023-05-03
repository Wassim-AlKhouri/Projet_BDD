SELECT DISTINCT p.nom
FROM pathologie p
WHERE p.NomSA = {placeholder}
GROUP BY p.nom
HAVING COUNT(DISTINCT Systeme_anatomique) = 1;

/*
La liste des pathologies qui peuvent être prise en charge 
par un seul type de spécialistes
*/
