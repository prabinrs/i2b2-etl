# llmEngine

- version : 0.0.1 
- stage : Draft

`llmEngine` uses a vLLM-backed LLM to detect whether user-specified terms (diagnoses, medications, tests) are mentioned in clinical notes stored in i2b2. It writes a boolean presence fact (`1` = found, `0` = not found) back into `observation_fact` for each patient × term pair.

---

## Prerequisites

### 1. Docker containers running

```bash
cd deployment/pg
docker compose up -d
```

Required containers: `i2b2-pg`, `i2b2-ml`

### 2. vLLM endpoint accessible

The engine calls an OpenAI-compatible vLLM HTTP endpoint. No API key is required.

Example endpoint used in testing:
```
https://prabinrs--vllm-gemma4-e2b-serve.modal.run

```

---

## Data Setup

### API based approach 
1. **create a concept for notes and llm extract** 
payloads: 
```{json}
{
  "path": "/i2b2/Notes/ClinicalNotes/",
  "code": "NOTE:CLINICAL",
  "type": "TEXTUAL"
}

```

```{json}
{
    "path": "/i2b2/LLM/NLP/Extract/",
    "code": "LLM:NLP:FOUND",
    "type": "TEXTUAL"
}
```

observation_facts 


### Seed a clinical note into i2b2 (direct SQL)

The engine reads notes from `observation_fact.observation_blob`. Each note must be linked to a concept path under your `note_concept_path`.

psql within docker into database i2b2 , if not sure about database name use -l will list all the database.  
```
docker exec [postgres docker id] -it psql -U postgres -d i2b2 
```

check schemas 
```{psql}
\dn
```

tables in scheam 
```
\dt [schema name].*
```

after confiming the tables and schema .. can run following command. 
```sql
-- Connect to the i2b2 database
SET search_path = i2b2demodata;

-- 1. Add the patient
INSERT INTO patient_dimension (patient_num, sex_cd, age_in_years_num, sourcesystem_cd)
VALUES (99001, 'M', 45, 'TEST_LLM')
ON CONFLICT DO NOTHING;

-- 2. Add a patient_mapping entry (required for the fact loader)
INSERT INTO patient_mapping (patient_ide, patient_ide_source, patient_num, patient_ide_status, project_id, sourcesystem_cd)
VALUES ('99001', 'TEST_LLM', 99001, 'A', 'demo', 'TEST_LLM')
ON CONFLICT DO NOTHING;

-- 3. Add the note concept
INSERT INTO concept_dimension (concept_path, concept_cd, name_char, sourcesystem_cd)
VALUES ('/i2b2/Notes/ClinicalNotes/', 'NOTE:CLINICAL', 'Clinical Notes', 'TEST_LLM')
ON CONFLICT DO NOTHING;

-- 4. Add the output concept (parent only; child codes are auto-created by llmEngine)
INSERT INTO concept_dimension (concept_path, concept_cd, name_char, sourcesystem_cd)
VALUES ('/i2b2/LLM/NLP/Extract/', 'LLM:NLP:FOUND', 'LLM NLP Extraction', 'TEST_LLM')
ON CONFLICT DO NOTHING;

-- 5. Insert the clinical note as a fact
INSERT INTO observation_fact
    (encounter_num, patient_num, concept_cd, provider_id, start_date,
     modifier_cd, instance_num, observation_blob, sourcesystem_cd)
VALUES
    (1, 99001, 'NOTE:CLINICAL', '@', '2024-01-01 00:00:00',
     '@', 1,
     'Patient is a 45-year-old male with type 2 diabetes. Currently on metformin 500mg twice daily. Last HbA1c was 7.2%.',
     'TEST_LLM')
ON CONFLICT DO NOTHING;
```

---

## Submitting a Job

Insert a row into the `job` table. The `input` column is a JSON object that configures the engine.

```sql
SET search_path = i2b2demodata;

INSERT INTO job (status, priority, project_name, input, job_type)
VALUES (
    'PENDING',
    1,
    'i2b2demodata',
    '{
        "path": "/i2b2/LLM/NLP/Extract/",
        "note_concept_path": "/i2b2/Notes/ClinicalNotes/",
        "search_terms": ["metformin", "HbA1c", "insulin"],
        "output_concept_code": "LLM:NLP:FOUND",
        "vllm_url": "https://prabinrs--vllm-gemma4-e2b-serve.modal.run",
        "model": "gemma4-e2b"
    }',
    'llm'
);
```

### Job input fields

| Field | Required | Description |
|---|---|---|
| `path` | yes | Concept path that identifies the output concept in i2b2 |
| `note_concept_path` | yes | Concept path prefix used to find clinical notes in `observation_fact` |
| `search_terms` | yes | List of terms to search for (diagnoses, medications, tests) |
| `output_concept_code` | yes | Base concept code for output facts (e.g. `LLM:NLP:FOUND`) |
| `vllm_url` | yes | Base URL of the vLLM server (without `/v1`) |
| `model` | yes | Model name as served by vLLM (e.g. `gemma4-e2b`) |

> **Note:** `priority` must be set (e.g. `1`). Jobs with `NULL` priority are never picked up by the job watcher.