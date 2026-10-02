-- Demo: add a second patient whose note mentions insulin but NOT metformin or HbA1c.
-- Safe to re-run (ON CONFLICT DO NOTHING).
SET search_path = i2b2demodata;

INSERT INTO patient_dimension (patient_num, sex_cd, age_in_years_num, sourcesystem_cd)
VALUES (99002, 'F', 62, 'TEST_LLM')
ON CONFLICT DO NOTHING;

INSERT INTO patient_mapping (patient_ide, patient_ide_source, patient_num, patient_ide_status, project_id, sourcesystem_cd)
VALUES ('99002', 'TEST_LLM', 99002, 'A', 'demo', 'TEST_LLM')
ON CONFLICT DO NOTHING;

INSERT INTO observation_fact
    (encounter_num, patient_num, concept_cd, provider_id, start_date,
     modifier_cd, instance_num, observation_blob, sourcesystem_cd)
VALUES
    (2, 99002, 'NOTE:CLINICAL', '@', '2024-02-01 00:00:00',
     '@', 1,
     'Patient is a 62-year-old female with type 1 diabetes managed with insulin glargine 20 units nightly. Denies chest pain.',
     'TEST_LLM')
ON CONFLICT DO NOTHING;
