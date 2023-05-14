SELECT DISTINCT p.pathologieNom
FROM Pathologie p
JOIN Diagnostic d ON d.pathologieNom = p.pathologieNom
WHERE d.specialite = '{placeholder1}'
GROUP BY p.pathologieNom
HAVING COUNT(DISTINCT d.specialite) = 1;