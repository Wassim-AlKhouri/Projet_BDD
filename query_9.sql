SELECT COUNT(DISTINCT d.medecinINAMI)
FROM DossierPatient d 
WHERE d.NISS = {placeholder1};