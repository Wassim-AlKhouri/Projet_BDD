SELECT DISTINCT p.pathologieNom
FROM Pathologie p
JOIN Diagnostic d ON d.pathologieNom = p.pathologieNom
WHERE d.specialite = {placeholder}
GROUP BY p.nom
HAVING COUNT(DISTINCT d.specialite) = 1;


--La liste des pathologies qui peuvent être prise en charge 
--par un seul type de spécialistes
