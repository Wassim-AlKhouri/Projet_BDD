SELECT DISTINCT m.INAMI, m.employeNom
FROM Medecin m
JOIN DossierPatient d ON d.medecinINAMI = m.INAMI
JOIN Medicament med ON med.medicamentNomCommercial=d.medicamentNomCommercial
JOIN SpecialiteSystemeAnatomique spsa ON spsa.systemeAnatomiqueNom = med.systemeAnatomiqueNom
JOIN Specialite sp ON sp.specialiteNom = spsa.specialiteNom
WHERE m.specialite <> sp.specialiteNom;