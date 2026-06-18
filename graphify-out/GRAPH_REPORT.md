# Graph Report - .  (2026-06-17)

## Corpus Check
- 0 files · ~999,999 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 889 nodes · 1803 edges · 95 communities (71 shown, 24 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 142 edges (avg confidence: 0.63)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_DB Connections & Auth|DB Connections & Auth]]
- [[_COMMUNITY_Concept Delete Operations|Concept Delete Operations]]
- [[_COMMUNITY_File Utils & Human Paths|File Utils & Human Paths]]
- [[_COMMUNITY_Concept REST API|Concept REST API]]
- [[_COMMUNITY_Concept API (Legacy)|Concept API (Legacy)]]
- [[_COMMUNITY_SQL Schema & Totalnum|SQL Schema & Totalnum]]
- [[_COMMUNITY_Config & Concept Utils|Config & Concept Utils]]
- [[_COMMUNITY_PM DataSource & App Loader|PM DataSource & App Loader]]
- [[_COMMUNITY_Encounter Transform|Encounter Transform]]
- [[_COMMUNITY_Base Config & Engine|Base Config & Engine]]
- [[_COMMUNITY_Fact Delete & Benchmarking|Fact Delete & Benchmarking]]
- [[_COMMUNITY_Project Management|Project Management]]
- [[_COMMUNITY_Bulk Uploader Core|Bulk Uploader Core]]
- [[_COMMUNITY_CRC DataSource & Fact Delete|CRC DataSource & Fact Delete]]
- [[_COMMUNITY_Loader App Helpers|Loader App Helpers]]
- [[_COMMUNITY_Common SQL Utils|Common SQL Utils]]
- [[_COMMUNITY_Encounter Mapping|Encounter Mapping]]
- [[_COMMUNITY_Observation Fact SQL|Observation Fact SQL]]
- [[_COMMUNITY_Encounter Delete|Encounter Delete]]
- [[_COMMUNITY_Patient Mapping|Patient Mapping]]
- [[_COMMUNITY_Fact Config & Delete|Fact Config & Delete]]
- [[_COMMUNITY_Project SQL Loader|Project SQL Loader]]
- [[_COMMUNITY_Undo & Validation|Undo & Validation]]
- [[_COMMUNITY_Concept Transform File|Concept Transform File]]
- [[_COMMUNITY_MIMIC Sample Files|MIMIC Sample Files]]
- [[_COMMUNITY_Bulk Uploader PG|Bulk Uploader PG]]
- [[_COMMUNITY_File Utils & Fact Upload|File Utils & Fact Upload]]
- [[_COMMUNITY_Deid Validation Utils|Deid Validation Utils]]
- [[_COMMUNITY_ML Dependencies|ML Dependencies]]
- [[_COMMUNITY_Runner & API Registry|Runner & API Registry]]
- [[_COMMUNITY_Patient Pipeline|Patient Pipeline]]
- [[_COMMUNITY_Job Orchestration|Job Orchestration]]
- [[_COMMUNITY_Loader Flask Routes|Loader Flask Routes]]
- [[_COMMUNITY_Patient Mapping Utils|Patient Mapping Utils]]
- [[_COMMUNITY_Fact Deidentification|Fact Deidentification]]
- [[_COMMUNITY_Loader Auth|Loader Auth]]
- [[_COMMUNITY_Docker Services|Docker Services]]
- [[_COMMUNITY_Date Parsing & Defaults|Date Parsing & Defaults]]
- [[_COMMUNITY_ML Jobs & Concepts|ML Jobs & Concepts]]
- [[_COMMUNITY_Fact API & Auth|Fact API & Auth]]
- [[_COMMUNITY_Patient Dimension DB|Patient Dimension DB]]
- [[_COMMUNITY_Logging|Logging]]
- [[_COMMUNITY_Loader Concept Routes|Loader Concept Routes]]
- [[_COMMUNITY_ETL Perform Layer|ETL Perform Layer]]
- [[_COMMUNITY_Encounter Deid & Bulk Upload|Encounter Deid & Bulk Upload]]
- [[_COMMUNITY_ML MIMIC HF Tests|ML MIMIC HF Tests]]
- [[_COMMUNITY_Project Config Helper|Project Config Helper]]
- [[_COMMUNITY_BCP Upload Helpers|BCP Upload Helpers]]
- [[_COMMUNITY_Concept Mapping|Concept Mapping]]
- [[_COMMUNITY_Patient Mapping DB|Patient Mapping DB]]
- [[_COMMUNITY_Runner Module|Runner Module]]
- [[_COMMUNITY_Patient Subdomain|Patient Subdomain]]
- [[_COMMUNITY_BCP SQL Utils|BCP SQL Utils]]
- [[_COMMUNITY_Deployment & Docker Docs|Deployment & Docker Docs]]
- [[_COMMUNITY_Loader Auth Routes|Loader Auth Routes]]
- [[_COMMUNITY_Loader Derived Jobs|Loader Derived Jobs]]
- [[_COMMUNITY_Log Utilities|Log Utilities]]
- [[_COMMUNITY_ML Clean Start Script|ML Clean Start Script]]
- [[_COMMUNITY_Concept Validation|Concept Validation]]
- [[_COMMUNITY_Setup Module|Setup Module]]
- [[_COMMUNITY_Runner Entry|Runner Entry]]
- [[_COMMUNITY_Field Length Constants|Field Length Constants]]
- [[_COMMUNITY_Config Helper Module|Config Helper Module]]
- [[_COMMUNITY_Provider Dimension SQL|Provider Dimension SQL]]
- [[_COMMUNITY_Patient Config Helper|Patient Config Helper]]
- [[_COMMUNITY_Patient Mapping Loader|Patient Mapping Loader]]
- [[_COMMUNITY_Config Parser Append|Config Parser Append]]
- [[_COMMUNITY_GitLab Container|GitLab Container]]
- [[_COMMUNITY_IBM DB2 Container|IBM DB2 Container]]
- [[_COMMUNITY_MSSQL Container|MSSQL Container]]

## God Nodes (most connected - your core abstractions)
1. `Config` - 120 edges
2. `I2b2crcDataSource` - 117 edges
3. `I2b2metaDataSource` - 54 edges
4. `formatPath()` - 28 edges
5. `humanPathToCodedPath()` - 28 edges
6. `I2b2pmDataSource` - 27 edges
7. `_exception_response()` - 27 edges
8. `str_from_file()` - 23 edges
9. `getDataFrameInChunksUsingCursor()` - 23 edges
10. `AuthConfig` - 22 edges

## Surprising Connections (you probably didn't know these)
- `MIMIC Example ML Config JSON` --conceptually_related_to--> `OBSERVATION_FACT Table`  [INFERRED]
  sample_files/mimic_example.json → i2b2_cdi/resources/sql/create_partitoned_table_observation_facts_pg.sql
- `Config` --calls--> `create_diabetes_concept()`  [EXTRACTED]
  i2b2_cdi/config/config.py → tests/ML/test_ml_mimic_hf.py
- `ML Usecase Config (with Patient Sets)` --conceptually_related_to--> `Test - ML MIMIC Heart Failure`  [INFERRED]
  sample_files/ML/ML usecase.json → tests/ML/test_ml_mimic_hf.py
- `ML Usecase Config (with Patient Sets)` --conceptually_related_to--> `Test - ML Pima Diabetes`  [INFERRED]
  sample_files/ML/ML usecase.json → tests/ML/test_ml_pima.py
- `Clean Start Shell Script` --references--> `Docker Container - i2b2-ml`  [EXTRACTED]
  tests/ML/clean_start.sh → deployment/pg/docker-compose.yml

## Hyperedges (group relationships)
- **Concept CRUD Pipeline** — concept_API_processRequest, concept_API_postConcept, concept_API_getConcept, concept_API_deleteConcept, concept_API_editConcept, concept_API_generate_load_csv, concept_runner_mod_run, perform_concept_concept_load_from_dir [EXTRACTED 0.95]
- **Ontology Load Pipeline** — perform_concept_concept_load_from_dir, i2b2_ontology_helper_get_concept_ontology, i2b2_sql_helper_getOntologySql, i2b2_sql_helper_getMetaDataArr, i2b2_sql_helper_getTableAccessArr, bulk_uploader_BulkUploader [EXTRACTED 0.95]
- **Concept Module Runner Dispatch** — concept_runner_mod_run, perform_concept_concept_load_from_dir, perform_concept_delete_concepts, perform_concept_undo_concepts, concept_extract_concept_extract, concept_benchmark_concept_benchmark, concept_count_get_concept_count [EXTRACTED 1.00]
- **Common Utilities Layer** — bulk_uploader_BulkUploader, file_util_getConcatCsvAsDf, file_util_dirGlob, file_util_str_to_file, file_util_str_from_file, utils_total_time, utils_formatPath, constants_SUCCESS [INFERRED 0.85]

## Communities (95 total, 24 thin omitted)

### Community 0 - "DB Connections & Auth"
Cohesion: 0.06
Nodes (38): change_password, get_package_path(), str_from_file(), I2b2hiveDataSource, Provided connection to the i2b2hivedata database, execSql(), getDataFrameInChunks(), getPdfUsingCursor() (+30 more)

### Community 1 - "Concept Delete Operations"
Cohesion: 0.08
Nodes (50): getCodedPath(), concepts_delete_by_id(), delete(), delete_concepts_i2b2_demodata(), Delete the concepts from i2b2 instance, I2b2metaDataSource, Provided connection to the i2b2metadata database, getDataFrameInChunksUsingCursor() (+42 more)

### Community 2 - "File Utils & Human Paths"
Cohesion: 0.07
Nodes (49): getConcatCsvAsDf(), Globs files with fileSuffix from dirPath, merges them into a single pandas DataF, str_to_file(), generate_human_paths(), translatePath(), addMapToConceptDef(), filterErrors(), find_error_in_row() (+41 more)

### Community 3 - "Concept REST API"
Cohesion: 0.09
Nodes (42): formatPath(), deleteConcept(), editConcept(), generate_load_csv(), getConcept(), postConcept(), processRequest(), validateCodePath() (+34 more)

### Community 4 - "Concept API (Legacy)"
Cohesion: 0.09
Nodes (25): mkParentDir(), concept_API.deleteConcept(), concept_API.generate_load_csv(), concept_API.getConcept(), concept_API.postConcept(), concept_API.processRequest(), concept_benchmark(), concept_benchmark() (+17 more)

### Community 5 - "SQL Schema & Totalnum"
Cohesion: 0.12
Nodes (28): Create PostgreSQL i2b2 Metadata Tables, Create SQL Server i2b2 Metadata Tables, BuildTotalnumReport Function, pat_count_dimensions Function, pat_count_visits Function, random_normal Function, RunTotalnum Function, Helper Random Normal Function SQL (+20 more)

### Community 6 - "Config & Concept Utils"
Cohesion: 0.10
Nodes (23): humanPathToCodedPath Function, Config Class, dynamic_importer(), getArgs Function, get_config_modules(), getArgs(), getDefaultUploadid(), import_module_from_path() (+15 more)

### Community 7 - "PM DataSource & App Loader"
Cohesion: 0.20
Nodes (18): I2b2pmDataSource, Provided connection to the i2b2pmdata database, AuthConfig, AllDerivedJobsStatus, CheckDatabase, ConfigData, derivedConceptJob, GetFact (+10 more)

### Community 8 - "Encounter Transform"
Cohesion: 0.08
Nodes (12): Encounter TransformFile Class, do_transform(), The class provides the interface for transforming csv data to bcp file, TransformFile, Fact Transform File (CSV to BCP), csv_to_bcp(), The class provides the various methods for transforming csv data to bcp file, TransformFile (+4 more)

### Community 9 - "Base Config & Engine"
Cohesion: 0.13
Nodes (7): ABC, clean_json_string(), Config, BaseEngine, mlEngine, load_concepts(), load_facts()

### Community 10 - "Fact Delete & Benchmarking"
Cohesion: 0.18
Nodes (18): delete_facts_i2b2_demodata(), determine_concept_type(), get_type(), benchmarkTimeAnalysis(), execute_partitions(), fact_benchmark(), generate_plot(), get_path() (+10 more)

### Community 11 - "Project Management"
Cohesion: 0.10
Nodes (14): addI2b2Project, addI2b2ProjectWrapper, copyDemoData, delete_data, runTotalNum, upgradeProject (in addProject), I2b2DbGenerator, DB Table: crc_db_lookup (+6 more)

### Community 12 - "Bulk Uploader Core"
Cohesion: 0.12
Nodes (14): BulkUploader Class, SUCCESS Constant, str_from_file(), get_concept_ontology_from_i2b2metadata(), get_existing_Ont2(), getConceptDimSql(), getMetaDataArr(), getMetaDataSql() (+6 more)

### Community 13 - "CRC DataSource & Fact Delete"
Cohesion: 0.13
Nodes (10): I2b2crcDataSource, Provided connection to the i2b2demodata database, facts_delete_by_id(), update_job_status(), update_job_status(), apply_model(), create_patient_set(), Creates a patient set in i2b2 from a SQL query. (+2 more)

### Community 14 - "Loader App Helpers"
Cohesion: 0.16
Nodes (13): AsyncLoadDataTask, _error_response(), generate_new_concept_file(), Class provides the interface to run the data loading task in a thread, _sucess_response(), _sucess_response_with_validation_soft_error(), check_db_status(), get_upload_id_vol_flags() (+5 more)

### Community 15 - "Common SQL Utils"
Cohesion: 0.12
Nodes (12): execute_sql_script(), get_path_relative_to_package_root(), get_resource_absolute_path(), line_count(), path_leaf(), Wrapper method to execute the queries using sqlcmd command          Args:, Returns file name from absolute path      Args:        path (str): absolute file, Returns line count for provided file       Args:        path (str): absolute fil (+4 more)

### Community 16 - "Encounter Mapping"
Cohesion: 0.14
Nodes (7): create_encounter_mapping(), EncounterMapping, The class provides the interface for de-identifying i.e. (mapping src encounter, This method writes encounter mapping to the database table using pyodbc connecti, This method writes encounter mappings in a csv file          Args:             e, This method writes the list of rows to the bcp file using csv writer          Ar, MozillaEncounterMapping

### Community 17 - "Observation Fact SQL"
Cohesion: 0.17
Nodes (15): Create Indexes Observation Fact PostgreSQL, Create Partitioned Observation Facts Table PostgreSQL, Create Patient Dimension Temp Table PostgreSQL, Drop Indexes Observation Fact PostgreSQL, Benchmark: Get Count Observation Fact, Benchmark: Get Distinct Patient Num Obs Fact, Load Observation Fact From Numbered PostgreSQL, Load Patient Dimension From Facts PostgreSQL (+7 more)

### Community 18 - "Encounter Delete"
Cohesion: 0.19
Nodes (8): delete_encounters(), EncounterMapping Class, bcp_upload_encounter_mapping(), create_encounter_mapping(), load_encounters(), Load encounter mapping from the given encounetr or fact file to the i2b2 instanc, Upload the encounters data from bcp file to the i2b2 instance      Args:, mod_run()

### Community 19 - "Patient Mapping"
Cohesion: 0.16
Nodes (8): MozillaPatientMapping, get_patient_mapping_obj(), PatientMapping, This method writes patient mappings in a csv file          Args:             pat, This method  increments patient num by 1., This method writes the list of rows to the bcp file using csv writer          Ar, The class provides the interface for creating patient mapping i.e. (mapping src, This method writes patient mapping to the database table using pyodbc connection

### Community 20 - "Fact Config & Delete"
Cohesion: 0.26
Nodes (13): I2b2 CRC Data Source, Fact Config Helper, Fact Deletion, Determine Concept Type, Fact Benchmark, Fact Count, Fact Extraction, Fact Validation Helper (+5 more)

### Community 21 - "Project SQL Loader"
Cohesion: 0.23
Nodes (12): getcsv(), load_concepts_data(), load_concepts_from_SQL(), load_data_from_SQL(), load_facts_data(), load_facts_from_SQL(), This method passes all facts sql files from input dir to getcsv()          Args:, This method checks for data to be loaded based on argument passed in command (+4 more)

### Community 22 - "Undo & Validation"
Cohesion: 0.21
Nodes (13): Undo Operation, Validation Helper, Apply Build Model ML, Build Model ML Helper, Concept API (ML Build), ML API, ML Use Case (Legacy), ML Engine (+5 more)

### Community 23 - "Concept Transform File"
Cohesion: 0.18
Nodes (8): Concept TransformFile Class, csv_to_bcp(), This method writes the list of rows to the bcp file using csv writer          Ar, Returns the type of value provided          Args:             x (type): value/in, Convert the csv file to bcp file and provide the path to the bcp file      Args:, The class provides the various methods for transforming csv data to bcp file, This method transforms csv file to bcp, Error records will be logged to log file, TransformFile

### Community 24 - "MIMIC Sample Files"
Cohesion: 0.17
Nodes (11): blob, data_paths, feature_selection_count, label_paths, negative_patient_set, positive_patient_set, time_buffer, code (+3 more)

### Community 25 - "Bulk Uploader PG"
Cohesion: 0.18
Nodes (7): BulkUploader, Class provides the wrapper method on bcp tool, Wrapper method to execute the queries using PSQL command          Args:, bcp_upload_encounters(), Upload the encounters data from bcp file to the i2b2 instance     Args:, bcp_upload_patient_mapping(), Upload the encounters data from bcp file to the i2b2 instance      Args:

### Community 26 - "File Utils & Fact Upload"
Cohesion: 0.31
Nodes (8): dirGlob(), Globs files with fileSuffix from dirPath     Arguments:         dirPath {string}, validate_fact_files(), fact_load_from_dir(), load_facts(), load_patient_mapping(), load_patient_mapping_from_fact_file(), Load patient mapping from the given fact file to the i2b2 instance.      Args:

### Community 27 - "Deid Validation Utils"
Cohesion: 0.18
Nodes (7): is_length_exceeded(), Checks the length of the given value against given length exceeds or not      Ar, validatations(), MozillaDeidPatient, DeidPatient, The class provides the interface for de-identifying i.e. (mapping src patient id, validate_row()

### Community 28 - "ML Dependencies"
Cohesion: 0.22
Nodes (10): Flask Dependency, MLflow Dependency, Pandas Dependency, scikit-learn Dependency, XGBoost Dependency, Logistic Regression Model (scikit-learn), Pima Indians Diabetes Dataset, Full Requirements (+2 more)

### Community 29 - "Runner & API Registry"
Cohesion: 0.27
Nodes (10): Concept Runner, ETL Concepts REST API Endpoint, ETL Job REST API Endpoint, I2b2crcDataSource, App Helper (Async Data Load), QT_PATIENT_SET_COLLECTION Table, QT_QUERY_MASTER Table, Test Helper - create_patient_set (+2 more)

### Community 30 - "Patient Pipeline"
Cohesion: 0.33
Nodes (7): bcp_upload_patient_dimension(), load_patient_dimension(), load_patient_dimension_from_facts(), Load patients from the given patient file to the i2b2 instance using pyodbc., Upload the encounters data from bcp file to the i2b2 instance      Args:, mod_run(), load_patient_dimension_from_facts

### Community 31 - "Job Orchestration"
Cohesion: 0.27
Nodes (3): jobOrchestrator, computeJob(), initJob()

### Community 32 - "Loader Flask Routes"
Cohesion: 0.29
Nodes (5): allowed_file(), get_session_dirs(), PerformData, This method check for allowed file extension., This method allows api interface to load data.

### Community 33 - "Patient Mapping Utils"
Cohesion: 0.24
Nodes (6): delete_file_if_exists(), file_len(), create_patient_mapping(), create_patient_mapping_file_from_fact_file(), get_patient_mapping(), Convert mrn column in fact file into the mrn file     Args:         fact_file (:

### Community 34 - "Fact Deidentification"
Cohesion: 0.22
Nodes (5): Fact De-identification, DeidFact, The class provides the interface for de-identifying i.e. (mapping src patient id, Mozilla DeidFact (External), MozillaDeidFact

### Community 35 - "Loader Auth"
Cohesion: 0.36
Nodes (5): fetchUserResult(), Validate user session, encode_login(), get_sessionKey(), get_xml()

### Community 36 - "Docker Services"
Cohesion: 0.25
Nodes (8): Clean Start Shell Script, Docker Container - i2b2-etl, Docker Container - i2b2-jupyter, Docker Container - i2b2-ml, Docker Container - i2b2-pg (PostgreSQL 15.1), Docker Container - i2b2-wildfly, Job Watcher - i2b2_cdi.job.jobWatcher, i2b2-etl README

### Community 37 - "Date Parsing & Defaults"
Cohesion: 0.33
Nodes (5): parse_date(), This method checks for date format          Args:             _date (:obj:`str`,, This method checks for date format          Args:             _date (:obj:`str`,, validate_fact_row(), validate_header()

### Community 38 - "ML Jobs & Concepts"
Cohesion: 0.33
Nodes (6): ML Concept - Diabetes Mellitus Type 2, ML Concept - Diabetes Model (no patient sets), ML Job - Apply Model, ML Job - Build Model, ML Usecase Config (with Patient Sets), ML Usecase Config (without Patient Sets)

### Community 39 - "Fact API & Auth"
Cohesion: 0.40
Nodes (5): Fact REST API, Job API (REST), Auth Config (Session Validation), Authenticate User (i2b2 PM), i2b2 CDI Flask App (Main API)

### Community 40 - "Patient Dimension DB"
Cohesion: 0.40
Nodes (5): DB Table: patient_dimension, TransformFile, do_transform, bcp_upload_patient_dimension, load_patient_dimension

### Community 43 - "ETL Perform Layer"
Cohesion: 0.50
Nodes (4): Perform Encounter, Perform Fact (ETL Orchestration), Mozilla Perform Fact (External), Perform Patient

### Community 45 - "ML MIMIC HF Tests"
Cohesion: 0.50
Nodes (3): create_diabetes_concept(), load_model_from_base64(), Deserialize a scikit-learn model from a base64-encoded string.

### Community 46 - "Project Config Helper"
Cohesion: 0.83
Nodes (3): appendConfigParser(), get_random_string(), validate()

### Community 49 - "Patient Mapping DB"
Cohesion: 0.67
Nodes (3): DB Table: patient_mapping, bcp_upload_patient_mapping, load_patient_mapping_from_fact_file

### Community 52 - "Patient Subdomain"
Cohesion: 0.67
Nodes (3): Deid Patient, Delete Patient, Patient Mapping

## Knowledge Gaps
- **90 isolated node(s):** `ModuleType`, `code`, `path`, `type`, `description` (+85 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **24 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `I2b2crcDataSource` connect `CRC DataSource & Fact Delete` to `DB Connections & Auth`, `Concept Delete Operations`, `File Utils & Human Paths`, `Concept REST API`, `Concept API (Legacy)`, `Loader Flask Routes`, `Config & Concept Utils`, `PM DataSource & App Loader`, `Base Config & Engine`, `Fact Delete & Benchmarking`, `Loader Concept Routes`, `Encounter Deid & Bulk Upload`, `ML MIMIC HF Tests`, `Bulk Uploader PG`, `File Utils & Fact Upload`, `Patient Pipeline`, `Job Orchestration`?**
  _High betweenness centrality (0.198) - this node is a cross-community bridge._
- **Why does `Config` connect `Base Config & Engine` to `DB Connections & Auth`, `Concept Delete Operations`, `File Utils & Human Paths`, `Concept REST API`, `Concept API (Legacy)`, `Config & Concept Utils`, `PM DataSource & App Loader`, `Fact Delete & Benchmarking`, `CRC DataSource & Fact Delete`, `Loader App Helpers`, `Encounter Delete`, `Project SQL Loader`, `Concept Transform File`, `Patient Pipeline`, `Job Orchestration`, `Loader Flask Routes`, `Loader Auth`, `Loader Concept Routes`, `ML MIMIC HF Tests`?**
  _High betweenness centrality (0.156) - this node is a cross-community bridge._
- **Why does `total_time()` connect `Encounter Deid & Bulk Upload` to `Patient Mapping Utils`, `Fact Deidentification`, `Encounter Transform`, `Common SQL Utils`, `Encounter Delete`, `File Utils & Fact Upload`, `Deid Validation Utils`, `Patient Pipeline`?**
  _High betweenness centrality (0.097) - this node is a cross-community bridge._
- **Are the 23 inferred relationships involving `Config` (e.g. with `TransformFile` and `BaseEngine`) actually correct?**
  _`Config` has 23 INFERRED edges - model-reasoned connections that need verification._
- **Are the 21 inferred relationships involving `I2b2crcDataSource` (e.g. with `BulkUploader` and `DataSource`) actually correct?**
  _`I2b2crcDataSource` has 21 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `I2b2metaDataSource` (e.g. with `BulkUploader` and `DataSource`) actually correct?**
  _`I2b2metaDataSource` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `humanPathToCodedPath()` (e.g. with `getDerivedConcept()` and `deleteDerivedConcept()`) actually correct?**
  _`humanPathToCodedPath()` has 4 INFERRED edges - model-reasoned connections that need verification._