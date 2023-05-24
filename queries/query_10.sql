SELECT DISTINCT d.medicamentNomCommercial
FROM DossierPatient d
WHERE NOT EXISTS (
  SELECT 1
  FROM DossierPatient d2
  WHERE d2.medicamentNomCommercial = d.medicamentNomCommercial
    AND d2.datePrescription > '{placeholder1}'
)