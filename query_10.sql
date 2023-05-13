SELECT DISTINCT d.medicamentNomCommercial
FROM DossierPatient d
WHERE d.datePrescription <= {placeholder}

--La liste de médicament n’étant plus prescrit depuis 
--une date spécifique

