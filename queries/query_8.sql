SELECT d.pathologieNom
FROM Diagnostic d
GROUP BY d.pathologieNom
ORDER BY COUNT(*) DESC
LIMIT 1