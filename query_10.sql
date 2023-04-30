SELECT DISTINCT med.NomC
FROM Medicament med
JOIN Prescription p ON med.NomC = p.NomC
JOIN traitement t ON t.DCI=m.DCI
WHERE t.Date_de_debut <= {placeholder}

/*
La liste de médicament n’étant plus prescrit depuis 
une date spécifique
*/
