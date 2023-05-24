WITH recursive years AS (
  SELECT 1950 AS year
  UNION ALL
  SELECT year + 10
  FROM years
  WHERE year < YEAR(CURRENT_DATE()) 
)
SELECT year, medicamentNomCommercial
FROM (
  SELECT
    y.year,
    med.medicamentNomCommercial,
    ROW_NUMBER() OVER (PARTITION BY y.year ORDER BY COUNT(*) DESC) AS med_rank
  FROM
    Medicament med
    JOIN DossierPatient d ON d.medicamentNomCommercial = med.medicamentNomCommercial
    JOIN Patient p ON p.NISS = d.NISS
    JOIN years y ON y.year <= EXTRACT(YEAR FROM p.DateNaissance) AND y.year + 10 > EXTRACT(YEAR FROM p.DateNaissance)
  GROUP BY
    y.year,
    med.medicamentNomCommercial
  ORDER BY
    COUNT(*) DESC,
    y.year DESC
) ranked
WHERE med_rank = 1
ORDER BY year DESC;