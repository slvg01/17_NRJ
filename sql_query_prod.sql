DROP TABLE IF EXISTS prod_full2;

SELECT *
INTO prod_full2
FROM (
	SELECT 
  		CASE 
			WHEN fuelcode = 'LF' THEN 'Other'
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


	UNION 

	
	SELECT 
		CASE 
			WHEN fueltypepublication = 'Wind Offshore' THEN 'Wind'
			WHEN fueltypepublication = 'Wind Onshore' THEN 'Wind'
			WHEN fueltypepublication = 'Water' THEN 'Water'
			WHEN fueltypepublication = 'Other Fuel' THEN 'Other'
			WHEN fueltypepublication = 'Other' THEN 'Other'
			WHEN fueltypepublication = 'Nuclear' THEN 'Nuclear'
			WHEN fueltypepublication = 'Natural Gas' THEN 'Natural Gas'
			WHEN fueltypepublication = 'Solar' THEN 'Solar'
			WHEN fueltypepublication = 'Biofuels' THEN 'Biofuels'
			ELSE 'Unknown'  
		END AS fuel_type,
		DATEADD(HOUR, 4 * (DATEDIFF(HOUR, 0, datetime) / 4), 0) AS window_start,
		AVG(generatedpower) AS generated_power,
		AVG(totalgeneratedpower) AS total_generated_power
	FROM prod_new
	GROUP BY DATEADD(HOUR, 4 * (DATEDIFF(HOUR, 0, datetime) / 4), 0), fueltypepublication

) AS alignement_query;
