from i2b2_cdi.database.cdi_database_connections import I2b2crcDataSource
from i2b2_cdi.database.cdi_db_executor import getDataFrameInChunksUsingCursor
from loguru import logger
import requests
from datetime import datetime


def get_notes(config, note_concept_path):
    """Fetch clinical notes from observation_fact.observation_blob.

    Queries all facts whose concept_cd belongs to any concept under
    note_concept_path and returns rows that have non-empty note text.

    Returns list of dicts: {patient_num, encounter_num, note_text, start_date}
    """
    crc_ds = I2b2crcDataSource(config)
    path_pattern = note_concept_path.rstrip('/') + '/%'

    query = """
        SELECT o.patient_num,
               o.encounter_num,
               o.observation_blob AS note_text,
               o.start_date
        FROM   observation_fact o
        JOIN   concept_dimension c ON o.concept_cd = c.concept_cd
        WHERE  c.concept_path LIKE %(params)s
          AND  o.observation_blob IS NOT NULL
          AND  o.observation_blob <> ''
    """

    with crc_ds as cursor:
        try:
            df = getDataFrameInChunksUsingCursor(
                cursor, query, path_pattern
            )
            logger.info('Fetched {} clinical notes for path: {}', len(df), note_concept_path)
            return df.to_dict(orient='records')
        except Exception as e:
            logger.exception('Error fetching clinical notes: {}', e)
            return []


def extract_presence(notes, search_terms, vllm_url, model):
    """Call vLLM chat completions API to detect term presence in each note.

    For each (note, term) pair, sends a yes/no prompt to the vLLM endpoint.
    Aggregates per patient: a term is marked True if found in ANY note for
    that patient.

    Returns: {patient_num: {term: bool, ...}, ...}
    """
    endpoint = vllm_url.rstrip('/') + '/v1/chat/completions'
    results = {}

    for note in notes:
        patient_num = note['patient_num']
        note_text = note['note_text']

        if patient_num not in results:
            results[patient_num] = {term: False for term in search_terms}

        for term in search_terms:
            # Skip API call if already confirmed present for this patient
            if results[patient_num][term]:
                continue

            prompt = _build_prompt(note_text, term)
            try:
                response = requests.post(
                    endpoint,
                    json={
                        'model': model,
                        'messages': [{'role': 'user', 'content': prompt}],
                        'max_tokens': 10,
                        'temperature': 0,
                    },
                    timeout=30,
                )
                response.raise_for_status()
                answer = (
                    response.json()['choices'][0]['message']['content']
                    .strip()
                    .lower()
                )
                if answer.startswith('yes'):
                    results[patient_num][term] = True
            except Exception as e:
                logger.warning(
                    'vLLM call failed for patient {} term {}: {}',
                    patient_num, term, e,
                )

    logger.info(
        'Extraction complete: {} patients, {} terms',
        len(results), len(search_terms),
    )
    return results


def ensure_concepts(config, parent_concept_code, search_terms, parent_concept_path):
    """Insert child concept codes into concept_dimension if they don't already exist.

    For each search term, creates a concept like:
      concept_cd  = LLM:NLP:FOUND:metformin
      concept_path = /i2b2/LLM/NLP/Extract/metformin/
      name_char   = LLM NLP: metformin

    This ensures fact validation passes when loading output facts.
    """
    crc_ds = I2b2crcDataSource(config)
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    parent_path = parent_concept_path.rstrip('/') + '/'

    with crc_ds as cursor:
        for term in search_terms:
            safe_term = term.replace(' ', '_')
            concept_cd   = '{}:{}'.format(parent_concept_code, safe_term)
            concept_path = '{}{}/'.format(parent_path, safe_term)
            name_char    = 'LLM NLP: {}'.format(term)
            try:
                cursor.execute(
                    """
                    INSERT INTO concept_dimension
                        (concept_path, concept_cd, name_char, update_date, download_date, import_date, sourcesystem_cd)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (concept_path) DO NOTHING
                    """,
                    (concept_path, concept_cd, name_char, now, now, now, 'LLM_ENGINE'),
                )
                logger.debug('Ensured concept: {} -> {}', concept_cd, concept_path)
            except Exception as e:
                logger.warning('Could not insert concept {}: {}', concept_cd, e)

    logger.info('Ensured {} child concepts under {}', len(search_terms), parent_concept_code)


def _build_prompt(note_text, term):
    return (
        f"Clinical note:\n{note_text}\n\n"
        f"Question: Is '{term}' explicitly mentioned or clearly implied in this note?\n"
        f"Answer with only 'yes' or 'no'."
    )
