DROP TABLE IF EXISTS installed_power_full;

SELECT *
INTO installed_power_full
FROM (
	SELECT 
  		CASE 
			WHEN fuelcode = 'LF' THEN 'Other Fuels'
			WHEN fuelcode = 'NG' THEN 'Natural Gas'
			WHEN fuelcode = 'NU' THEN 'Nuclear'
			WHEN fuelcode = 'Other' THEN 'Other'
			WHEN fuelcode = 'WA' THEN 'Water'
			WHEN fuelcode = 'WI' THEN 'Wind'
			WHEN fuelcode = 'SO' THEN 'Solar'
			WHEN fuelcode = 'CP' THEN 'CP'
			ELSE 'Unknown'  
		END AS fuel_type,
		Date AS date,
		ARP AS provider,
		productionunitname AS unit_name,
		generationunittype AS unit_type,
		productionunitnominalpower AS unit_power
	FROM installed_power_old
	

	UNION 

	
	SELECT 
		CASE 
			WHEN fueltypepublication = 'Wind Offshore' THEN 'Wind'
			WHEN fueltypepublication = 'Wind Onshore' THEN 'Wind'
			WHEN fueltypepublication = 'Water' THEN 'Water'
			WHEN fueltypepublication = 'Other Fossil Fuels' THEN 'Other Fuels'
			WHEN fueltypepublication = 'Other' THEN 'Other'
			WHEN fueltypepublication = 'Nuclear' THEN 'Nuclear'
			WHEN fueltypepublication = 'Natural Gas' THEN 'Natural Gas'
			WHEN fueltypepublication = 'Solar' THEN 'Solar'
			WHEN fueltypepublication = 'Biofuels' THEN 'Biofuels'
			ELSE 'Unknown'  
		END AS fuel_type,
		Date AS date,
		provider,
		technicalunit AS unit_name,
		unittype AS unit_type,
		technicalpmax AS unit_power
		 
	FROM installed_power_new
	WHERE Date IN ('2024-06-01', '2025-01-01')


) AS alignement_query;
