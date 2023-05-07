SELECT COUNT(DISTINCT d.medecinINAMI)
FROM DossierPatient d 
WHERE d.NISS = {placeholder};

/*
Pour chaque patient,le nombre de médecin lui ayant prescrit
un médicament
*/
