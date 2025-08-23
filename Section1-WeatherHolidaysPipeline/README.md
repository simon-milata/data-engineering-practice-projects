# Section 1: API Integration and Data Pipeline

In this section, you'll build a data pipeline that integrates weather and public holiday data to enable analysis of how holidays affect weather observation patterns. 

**Task Description**

Create a data pipeline that:

* Extracts historical weather data and public holiday data from two different APIs.

* Transforms and merges the data.

* Models the data into a dimensional schema suitable for a data warehouse.

* Enables analysis of weather conditions on public holidays versus regular days for any given country. API Integration Requirements

*  API 1: Open-Meteo Weather API

    * A free, open-source weather API without authentication.

    * Documentation: https://open-meteo.com/en/docs/historical-weather-api

* API 2: Nager.Date Public Holiday API

    * A free API to get public holidays for any country.

    * Documentation: https://date.nager.at/api Data Pipeline Requirements

* Data Extraction:

    * Write modular code to extract historical daily weather data (e.g., temperature max/min, precipitation) for a major city and public holidays for the corresponding country for the last 5 years.

    * Implement robust error handling and a configuration mechanism (e.g., for city/country).

* Data Transformation:

    * Clean and normalize the data from both sources.

    * Combine the two datasets, flagging dates that are public holidays.

* Data Loading:

    * Design a set of tables for a data warehouse to store this data.

    * The model should allow analysts to easily compare weather metrics on holidays vs. non-holidays.

    * Create the SQL DDL for these tables. Deliverables

* Python code for the data extraction, transformation, and loading logic.

* SQL schema (.sql file) for your data warehouse tables, including keys and indexes.

* Documentation explaining:

    * Your overall data pipeline design.

    * The rationale behind your data model.

    * How your solution handles potential issues like API downtime or data inconsistencies.

    * How you would schedule and monitor this pipeline in a production environment (e.g., using Airflow, cron, etc.).

