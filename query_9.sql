SELECT p.nom,p.prenom,COUNT(DISTINCT d.medecinINAMI)
FROM DossierPatient d 
JOIN Patient p ON p.NISS = d.NISS
GROUP BY p.NISS
ORDER BY COUNT(DISTINCT d.medecinINAMI) DESC, p.nom ASC, p.prenom ASC