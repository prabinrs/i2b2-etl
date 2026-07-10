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

---

## Monitoring the Job

The `jobWatcher` polls the `job` table every 10 seconds and automatically picks up `PENDING` jobs.

### Check job status

```sql
SET search_path = i2b2demodata;
SELECT id, status, output FROM job ORDER BY id DESC LIMIT 5;
```

Status values: `PENDING` → `PROCESSING` → `COMPLETED` / `ERROR`

### Watch live logs

```bash
docker logs i2b2-ml -f
```

A successful run looks like:

```
INFO  | llmEngine.py:run | Running llmEngine, 5 for conceptPath:/i2b2/LLM/NLP/Extract/
INFO  | llmHelper:get_notes | Fetched 1 clinical notes for path: /i2b2/Notes/ClinicalNotes/
INFO  | llmHelper:extract_presence | Extraction complete: 1 patients, 3 terms
INFO  | llmHelper:ensure_concepts | Ensured 3 child concepts under LLM:NLP:FOUND
SUCCESS | mozilla_perform_fact:load_facts | Completed ✔
SUCCESS | jobWatcher:computeJob | COMPLETED llm Job for job_id = 5 for project = i2b2demodata
```

---

## Verifying the Output

### Check facts in observation_fact

```sql
SET search_path = i2b2demodata;

SELECT patient_num, concept_cd, tval_char AS value
FROM observation_fact
WHERE concept_cd LIKE 'LLM:NLP:FOUND:%'
ORDER BY concept_cd;
```

Expected output:

```
 patient_num |       concept_cd        | value
-------------+-------------------------+-------
  1000000135 | LLM:NLP:FOUND:HbA1c     | 1
  1000000135 | LLM:NLP:FOUND:insulin   | 0
  1000000135 | LLM:NLP:FOUND:metformin | 1
```

- `tval_char = 1` → term was found in at least one note for this patient
- `tval_char = 0` → term was not found

> **Note:** The `patient_num` in the output will be a de-identified ID assigned by the fact loader pipeline, not the original `99001`. This is expected behaviour.

### Check auto-created concept codes

```sql
SET search_path = i2b2demodata;

SELECT concept_cd, name_char, concept_path
FROM concept_dimension
WHERE concept_cd LIKE 'LLM:NLP:FOUND:%';
```

---

## How It Works Internally

```
job.input (JSON)
       │
       ▼
llmEngine.run()
       │
       ├─ get_job_inputs(jobId)
       │       reads JSON config from job table
       │
       ├─ llmHelper.get_notes(config, note_concept_path)
       │       SELECT observation_blob FROM observation_fact
       │       JOIN concept_dimension WHERE concept_path LIKE '<path>%'
       │
       ├─ llmHelper.extract_presence(notes, search_terms, vllm_url, model)
       │       POST /v1/chat/completions for each (note, term) pair
       │       returns {patient_num: {term: True/False}}
       │
       ├─ llmHelper.ensure_concepts(config, output_concept_code, search_terms, path)
       │       INSERT INTO concept_dimension for each sub-term concept
       │       (e.g. LLM:NLP:FOUND:metformin) — skips if already exists
       │
       └─ send_facts(df)
               writes CSV → fact_runner → observation_fact
               one row per patient × term with value 1 or 0
```

---

## Running Unit Tests

```bash
docker exec i2b2-ml bash -c "
  cd /usr/src/app &&
  source .venv/bin/activate &&
  PYTHONPATH=/usr/src/app python -m pytest tests/ML/test_llm_engine.py -v
"
```

All 10 tests should pass (vLLM calls and DB calls are mocked).

---

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| Job stays `PENDING` forever | `priority` is NULL | Set `priority = 1` on the job row |
| `No clinical notes found` | Wrong `note_concept_path` or missing note | Check `observation_blob` is not empty for that concept path |
| Facts not in `observation_fact` | Concept code missing from `concept_dimension` | Fixed automatically by `ensure_concepts()` in the current code |
| `ModuleNotFoundError: Mozilla` | PYTHONPATH not set | Ensure `PYTHONPATH=/usr/src/app` in container environment |
| vLLM timeout | Modal endpoint cold-starting | Retry — first call may take 30–60s to warm up |
| Patient not found after load | Missing `patient_mapping` entry | Insert a `patient_mapping` row linking `patient_ide` to `patient_num` |
