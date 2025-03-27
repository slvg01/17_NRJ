SELECT *
INTO prod_full
FROM (
	SELECT 
  		CASE 
			WHEN fuelcode = 'LF' THEN 'Other Fuel'
			WHEN fuelcode = 'NG' THEN 'Natural Gas'
			WHEN fuelcode = 'NU' THEN 'Nuclear'
			WHEN fuelcode = 'Other' THEN 'Other'
			WHEN fuelcode = 'WA' THEN 'Water'
			WHEN fuelcode = 'WI' THEN 'Wind'
			WHEN fuelcode = 'SO' THEN 'Solar'
			ELSE 'Unknown'  
		END AS fuel_type,
		DATEADD(HOUR, 4 * (DATEDIFF(HOUR, 0, datetime) / 4), 0) AS window_start,
		AVG(generatedpower) AS generated_power,
		AVG(totalgeneratedpower) AS total_generated_power
	FROM prod_old
	WHERE fuelcode <> 'CP'
	GROUP BY DATEADD(HOUR, 4 * (DATEDIFF(HOUR, 0, datetime) / 4), 0), fuelcode
	--ORDER BY window_start, fuel_type;

	UNION 

	SELECT 
  		fueltypepublication AS fuel_type,
		DATEADD(HOUR, 4 * (DATEDIFF(HOUR, 0, datetime) / 4), 0) AS window_start,
		AVG(generatedpower) AS generated_power,
		AVG(totalgeneratedpower) AS total_generated_power
	FROM prod_new
	GROUP BY DATEADD(HOUR, 4 * (DATEDIFF(HOUR, 0, datetime) / 4), 0), fueltypepublication
	--ORDER BY window_start, fuel_type;
) AS alignement_query;
