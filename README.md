# Data Engineering Practice Projects

A collection of practice projects to build, test, and deploy data pipelines, data models, and architectures. Each project focuses on a different aspect of data engineering, from API integration to data warehousing and real-time streaming.

---

## Projects

### 1. Weather & Public Holidays Pipeline
- **Goal:** Build a data pipeline that extracts weather data and public holiday data, merges them, and stores in a dimensional schema for analysis.
- **Key Features:**
  - Extract historical weather and holiday data from APIs.
  - Transform and merge datasets with date alignment.
  - Load into a dimensional schema with holiday flags.

### 2. E-commerce Data Modeling
- **Goal:** Model sales, inventory, and product data into a dimensional warehouse.
- **Key Features:**
  - Star/snowflake schema for facts and dimensions.
  - Handles slowly changing dimensions (SCD) for product prices.
  - Supports mixed granularity (transactional vs snapshot).

### 3. Product Recommendation Architecture
- **Goal:** Design a scalable architecture to support real-time and batch recommendation engines.
- **Key Features:**
  - Event ingestion, enrichment, and processing pipelines.
  - Supports both batch and real-time analytics.
  - Diagrammed architecture with suggested technologies and monitoring strategies.
