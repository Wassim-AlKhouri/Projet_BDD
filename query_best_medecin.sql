SELECT m.employeNOM, COUNT(dp.medecinINAMI)
FROM Medecin m
JOIN Dossier patient dp ON dp.medecinINAMI = m.INAMI
JOIN Diagnostic d ON d.NISS = dp.NISS
WHERE d.pathologieNom = {placeholder}
GROUP BY dp.medecinINAMI
ORDER BY COUNT(dp.medecinINAMI) DESC, m.employeNOM ASC
