SELECT p.Nom
FROM Pathologie p
JOIN Diagnostic d ON p.Nom = d.Pathologie_Nom
GROUP BY p.Nom
ORDER BY COUNT(*) DESC
LIMIT 1;

/*
Quelle est la pathologie la plus diagnostiquée
*/