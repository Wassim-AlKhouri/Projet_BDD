SELECT s.Nom
FROM systeme_anatomique s
JOIN medecin m ON s.Nom = m.NomSA
JOIN prescription p ON p.INAMI_med = m.INAMI
GROUP BY s.Nom
ORDER BY COUNT(*) DESC
LIMIT 1;
/*
La spécialité de médecins pour laquelle les médecins 
prescrivent le plus de médicaments
*/