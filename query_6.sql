SELECT DISTINCT m.INAMI, m.employeNom,
FROM Medecin m
JOIN DossierPatient d ON d.medecinINAMI = m.INAMI
JOIN Medicament med ON med.medicamentNomCommercial=d.medicamentNomCommercial
JOIN SpecialiteSystèmeAnatomique spsa ON spsa.systèmeAnatomiqueNom = med.systèmeAnatomiqueNom
JOIN Specialite sp ON sp.specialiteNom = spsa.specialiteNom
WHERE m.specialite <> sp.specialiteNom;

/*
La liste des médecins ayant prescrit des médicaments 
ne relevant pas de leur spécialité
*/