⚡ *This project is a work in progress!* ⚡

# API-SSMS-SQL-Tableau Project on Belgium Energy Production

## 🚀 Project Overview

This project aims to:

- Retrieve data from ([Elia's OpenData platform](https://opendata.elia.be/)) and at a later stage from ([ENTSO new transparency platform](https://newtransparency.entsoe.eu/)) via their API concerning:
  - **Electricity production and mix in Belgium** (datasets: [ODS177](https://opendata.elia.be/explore/dataset/ods177/) and [ODS033](https://opendata.elia.be/explore/dataset/ods033/))
  - **Instantaneous grid load** (dataset: [ODS169](https://opendata.elia.be/explore/dataset/ods169/))
- Load and store these data in SSMS to create an SQL database
- Connect **Tableau** to this database to process and visualize the data effectively

## 📂 In this Repo, You Will Find:

✅ A **PDF export** of the Tableau dashboard [(Visuals.pdf)](https://github.com/slvg01/84.16_Belgium_nrj_grid/blob/main/nrj_mix_work_in_progress.pdf)  
✅ The **Python script** to fetch data via API and load it into SQL  
✅ The **requirements.txt** file listing the necessary libraries to run the script  

## 📌 Technical Details

- **Python Version:** 3.12.9
- **Database:** SQL Server (SSMS)
- **Visualization Tool:** Power BI then Tableau  

## ⚡ Major Changes to Data Merging

In order to provide a better overview of the energy production in Belgium, the following major adjustments were made in the data:

- The **old** data (pre-May 2024) and **new** data (post-May 2024) have been aligned and merged for a smoother comparison.
- The **LF** (Other Fuel) category has been consolidated with **Other** as it was marginal.
- The **Wind Offshore** and **Wind Onshore** data from the new dataset have been consolidated into a single **Wind** category due to the relatively small contribution of **Wind Onshore**.
- These modifications are aimed at providing a clearer view of the energy production evolution over time.

## 📊 Fuel Type Mapping for `prod_old` and `prod_new` Datasets

This table reflects the fuel type transformations applied in the SQL query to merge the old and new datasets. The fuel codes are mapped as follows:

| **Fuel Code (prod_old)** | **Mapped Fuel Type**  | **Fuel Type (prod_new)**  | **Mapped Fuel Type**  |
|--------------------------|-----------------------|---------------------------|-----------------------|
| LF                       | Other                 | Wind Offshore             | Wind                  |
| NG                       | Natural Gas           | Wind Onshore              | Wind                  |
| NU                       | Nuclear               | Water                     | Water                 |
| Other                    | Other                 | Other Fuel                | Other                 |
| WA                       | Water                 | Other                     | Other                 |
| WI                       | Wind                  | Nuclear                   | Nuclear               |
| SO                       | Solar                 | Natural Gas               | Natural Gas           |
|                          |                       | Solar                     | Solar                 |
|                          |                       | Biofuels                  | Biofuels              |

---

⚡ *This project is a work in progress!* ⚡
