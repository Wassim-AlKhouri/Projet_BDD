SELECT DISTINCT d.medicamentNomCommercial
FROM DossierPatient d
WHERE d.datePrescription <= {placeholder1}