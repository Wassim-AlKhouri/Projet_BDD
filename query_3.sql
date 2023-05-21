SELECT s.specialiteNom
FROM Specialite s
JOIN SpecialiteSystemeAnatomique a ON s.specialiteNom = a.SpecialiteNom
JOIN Medicament m ON m.systemeAnatomiqueNom=a.systemeAnatomiqueNom
JOIN DossierPatient d ON d.medicamentNomCommercial=m.medicamentNomCommercial
GROUP BY s.specialiteNom
ORDER BY COUNT(DISTINCT m.medicamentNomCommercial) DESC
LIMIT 1