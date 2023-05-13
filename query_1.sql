SELECT DISTINCT m.medicamentNomCommercial
FROM Medicament m
WHERE m.DCI = {placeholder}
ORDER BY m.medicamentNomCommercial ASC, m.conditionnement ASC;


--La liste des noms commerciaux de médicaments correspondant 
--à un nom en DCI,classés par 
--ordre alphabétique et taille de conditionnement.