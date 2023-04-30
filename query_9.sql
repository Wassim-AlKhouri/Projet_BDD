SELECT COUNT(DISTINCT m.INAMI)
FROM medecin m
JOIN prescription pr ON pr.INAMI_med = m.INAMI
JOIN patient p ON p.NISS = pr.NISS
WHERE p.NISS = "NISS du patient concerné";

/*
Pour chaque patient,le nombre de médecin lui ayant prescrit
un médicament
*/