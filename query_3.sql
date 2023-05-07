SELECT s.specialiteNom
FROM Specialite s
JOIN SpecialiteSystèmeAnatomique a ON s.specialiteNom = a.SpecialiteNom
JOIN Medicament m ON m.systèmeAnatomiqueNom=a.systèmeAnatomiqueNom
JOIN DossierPatient d ON d.medicamentNomCommercial=m.medicamentNomCommercial
GROUP BY s.specialiteNom
ORDER BY COUNT(*) DESC
LIMIT 1;
/*
La spécialité de médecins pour laquelle les médecins 
prescrivent le plus de médicaments
*/