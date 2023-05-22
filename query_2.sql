SELECT p.pathologieNom
FROM Pathologie p 
WHERE p.specialiteNom IN (
    SELECT DISTINCT ssa.specialiteNom
    FROM SpecialiteSystemeAnatomique ssa
    WHERE NOT EXISTS (
        SELECT *
        FROM SpecialiteSystemeAnatomique ssa2
        WHERE ssa.systemeAnatomiqueNom = ssa2.systemeAnatomiqueNom
        AND ssa.specialiteNom != ssa2.specialiteNom
    )
)