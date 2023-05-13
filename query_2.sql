SELECT DISTINCT p.pathologieNom
FROM Pathologie p
JOIN Diagnostic d ON d.pathologieNom = p.pathologieNom
WHERE d.specialite = '{placeholder1}'
GROUP BY p.nom
HAVING COUNT(DISTINCT d.specialite) = 1;