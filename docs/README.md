# Data Engineering Assessment

Welcome!  
This exercise evaluates your core **data-engineering** skills:

| Competency | Focus                                                         |
| ---------- | ------------------------------------------------------------- |
| SQL        | relational modelling, normalisation, DDL/DML scripting        |
| Python ETL | data ingestion, cleaning, transformation, & loading (ELT/ETL) |

---

## 0 Prerequisites & Setup

> **Allowed technologies**

- **Python ≥ 3.8** – all ETL / data-processing code
- **MySQL 8** – the target relational database
- **Lightweight helper libraries only** (e.g. `pandas`, `mysql-connector-python`).  
  List every dependency in **`requirements.txt`** and justify anything unusual.
- **No ORMs / auto-migration tools** – write plain SQL by hand.

---

## 1 Clone the skeleton repo

```
git clone https://github.com/100x-Home-LLC/data_engineer_assessment.git
```

✏️ Note: Rename the repo after cloning and add your full name.

**Start the MySQL database in Docker:**

```
docker-compose -f docker-compose.initial.yml up --build -d
```

- Database is available on `localhost:3306`
- Credentials/configuration are in the Docker Compose file
- **Do not change** database name or credentials

For MySQL Docker image reference:
[MySQL Docker Hub](https://hub.docker.com/_/mysql)

---

### Problem

- You are provided with a raw JSON file containing property records is located in data/
- Each row relates to a property. Each row mixes many unrelated attributes (property details, HOA data, rehab estimates, valuations, etc.).
- There are multiple Columns related to this property.
- The database is not normalized and lacks relational structure.
- Use the supplied Field Config.xlsx (in data/) to understand business semantics.

### Task

- **Normalize the data:**

  - Develop a Python ETL script to read, clean, transform, and load data into your normalized MySQL tables.
  - Refer the field config document for the relation of business logic
  - Use primary keys and foreign keys to properly capture relationships

- **Deliverable:**
  - Write necessary python and sql scripts
  - Place your scripts in `sql/` and `scripts/`
  - The scripts should take the initial json to your final, normalized schema when executed
  - Clearly document how to run your script, dependencies, and how it integrates with your database.

**Tech Stack:**

- Python (include a `requirements.txt`)
  Use **MySQL** and SQL for all database work
- You may use any CLI or GUI for development, but the final changes must be submitted as python/ SQL scripts
- **Do not** use ORM migrations—write all SQL by hand

---

## Submission Guidelines

- Edit the section to the bottom of this README with your solutions and instructions for each section at the bottom.
- Place all scripts/code in their respective folders (`sql/`, `scripts/`, etc.)
- Ensure all steps are fully **reproducible** using your documentation
- Create a new private repo and invite the reviewer https://github.com/mantreshjain

---

**Good luck! We look forward to your submission.**

## Solutions and Instructions (Filed by Candidate)

# ETL Pipeline

This assignment is an end-to-end **ETL (Extract, Transform, Load)** pipeline built to process, clean, and normalize a real estate property dataset of 10,000 records. It is designed to handle messy categorical data, populate lookup tables, and load the cleaned dataset into a normalized **MySQL** database.

##  Project Structure

```
data_engineer_assessment/
   ├── data/
   │   ├── fake_property_data.json
   │   └── Field Config.xlsx
   ├── docs/               
   │   ├── images
   │   └── README.md
   ├── profiling/               # EDA and profiling reports
   │   ├── data_profiling.ipynb
   │   └── report.html
   ├── scripts/
   │  ├── config/                  # Config variables (DB creds, constants)
   │  │   └── config.py
   │  ├── extract/                 # Extraction logic
   │  │   └── extract.py
   │  ├── transform/               # Cleaning, normalization logic
   │  │   ├── columnsname.py
   │  │   └── transform.py.py
   │  ├── load/                    # Loaders to MySQL
   │  │   └── load.py
   │  ├── utils/                    # Logs for pipeline execution
   │  │   └── logger.py
   │  ├── etl.log          
   │  ├── main.py                  # Entry point to run the pipeline
   │  └── requirements.txt
   ├── sql/
   │   └── ddl_statements.sql       # sql ddl statements for table creation at the beggining
   ├── docker-compose.final.yml
   ├── docker-compose.initial.yml
   ├── Dockerfile.final_db
   └── Dockerfile.initial_db
```
## Data EDA and profiling
Data profiling has been carried out and following conclutions are made.
| Column Name                                                              | Unique Values | Clean Required?                      | Lookup Table? | Notes                                                  |
| ------------------------------------------------------------------------ | ------------- | ------------------------------------ | ------------- | ------------------------------------------------------ |
| `Reviewed_Status`                                                        | 10           |  Yes (e.g., typos, trailing spaces) |  Yes         | Categorical, inconsistent, frequently reused           |
| `Most_Recent_Status`                                                     | 12           |  Yes (`' Close '`, `'Cancel'`)      |  Yes         | Categorical, consistent usage                          |
| `Source`                                                                 | 7            | Yes (`' MLS'`, `'M L S'`)          |  Yes         | Slight inconsistencies in naming                       |
| `Market`                                                                 | 8            | Yes (`'Dalas'`, `'Chicgo'`)        |  Yes         | Misspellings, standardized location names              |
| `Occupancy`                                                              | 3             |  Yes                                |  No   | Can be stored as enum/boolean                          |
| `Flood`                                                                  | 3             |  Yes                                |  Yes         | Standard categorical field                             |
| `State`                                                                  | 59          |  No                                 |  No          | No action needed                   |
| `Property_Type`                                                          | 5             |  No                                 |  Yes   |                            |
| `Highway`, `Train`                                                       | 3             |  Yes                                | Yes         | Repeated spatial categories                            |
| `HTW`, `Pool`, `Commercial`, `Rent_Restricted`, `Seller_Retained_Broker` | 3             |  No                                 |  No(Boolean)   | Binary flags (Yes/No); direct mapping possible         |
| `Water`, `Sewage`, `Parking`                                             | 2–4           |  No                                 |  No.(ENUM)   | Low cardinality; lookup optional                       |
| `Bed`, `Bath`                                                            | Numeric       |  No                                 |  No          | Quantitative metrics                                   |
| `BasementYesNo`                                                          | 3             |  No                                 |  No.(Boolean)   | Can be directly mapped                                 |
| `Layout`                                                                 | 3–4           |  No                                 |  Yes         | Reusable layout categories                             |
| `Neighborhood_Rating`                                                    | 5             |  No                                 |  No          | Pure numeric score; no transformation needed           |
| `Selling_Reason`                                                         | 4             |  Yes                                | Yes         | Reusable categorized reasons                           |
| `Final_Reviewer`                                                         | 10            |  No                                 |  Yes         | Named users — potential for a reviewer dimension table |


## Database Schema and Design
- As per the requirements, data has been normalized to reduce redundancy and improve data integrity.
To achieve this, lookup tables have been created for columns containing repetitive or categorical values.
While normalization supports better maintainability, it can increase JOIN complexity, so it's a performance vs clarity trade-off that should be tuned based on business needs.
- Columns with Yes/No values are stored as boolean types (True/False) for performance and storage efficiency.
An alternative approach could have been the use of ENUM, but booleans are simpler and sufficient for this context.
- NULL values are retained in the dataset.
No imputation or row removal has been applied. This is intentional, as NULLs may carry valuable business insight, such as missing entries due to real-world absence or delays, and should not be discarded blindly.
#### Schema design:
![]()
![]()
## ETL Flow

1. **Extract**  
   Read raw JSON data containing property details.

2. **Transform**  
   - Clean typos, normalize spacing
   - Standardize `Yes`/`No` to boolean
   - Populate lookup tables for categorical fields
   - Map foreign keys

3. **Load**  
   Insert normalized data into MySQL using SQLAlchemy.

##  Key Cleaning Logic

- `Reviewed_Status`, `Market`, `Source`etc are cleaned using custom mappers.
- Boolean fields normalized from "Yes"/"No" to `True`/`False`.
- Lookup tables used to reduce redundancy for categorical columns.

# How to run ETL?
##  Configuration

Set database credentials and config parameters in `config/config.py`:

```python
#__Log configuration___
LOG_LEVEL = "DEBUG"  # or "INFO", "WARNING", "ERROR"
LOG_TO_CONSOLE = False
# ___ Database configurations___
USER_NAME = "db_user"
PASSWORD = "6equj5_db_user"
HOST = "127.0.0.1"
PORT = '3306'
DB_NAME = 'home_db'
```

##  Docker Run

To run with Docker Compose:

```bash
docker-compose -f docker-compose.initial.yml up --build -d
OR 
docker compose -f docker-compose.initial.yml up --build -d
```


MySQL container will initialize with:
- `MYSQL_DATABASE=home_db`
- `MYSQL_USER=db_user`

After few minutes docker up and running. Tables gets created based on file,
```
   ├── sql/
      └── ddl_statements.sql 
```
##  Usage
Go to the directory where `main.py`
```bash
python main.py /path/to/fake_property_data.json
```

All logs will be saved in `etl.log`.

##  Data Profiling

Detailed data profiling results are available under:

- `profiling/data_profiling.ipynb`
- `profiling/report.html`

##  Features

- Clean modular ETL design
- Lookup table support for normalization
- Custom logging
- Docker-compatible
