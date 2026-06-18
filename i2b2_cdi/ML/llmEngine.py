from i2b2_cdi.config.config import Config
from i2b2_cdi.job.BaseEngine import BaseEngine
from i2b2_cdi.ML.llmHelper import extract_presence, get_notes, ensure_concepts
from loguru import logger
import pandas as pd


class llmEngine(BaseEngine):

    def __init__(self, jobId=None):
        super().__init__()
        self.job_id = jobId

    def run(self, jobId, projectName, input, conceptCode, conceptPath, node, jobType):
        logger.info('Running {}, {} for conceptPath:{}', __class__.__name__, jobId, conceptPath)

        job_inputs = self.get_job_inputs(jobId)
        note_concept_path   = job_inputs['note_concept_path']
        search_terms        = job_inputs['search_terms']
        output_concept_code = job_inputs.get('output_concept_code', conceptCode)
        vllm_url            = job_inputs['vllm_url']
        model               = job_inputs.get('model', 'default')

        config = Config().new_config(argv=['project', 'add'])
        notes = get_notes(config, note_concept_path)

        if not notes:
            logger.warning('No clinical notes found for path: {}', note_concept_path)
            self.output = {}
            return

        results = extract_presence(notes, search_terms, vllm_url, model)

        # Ensure concept codes exist in concept_dimension before loading facts
        ensure_concepts(config, output_concept_code, search_terms, conceptPath)

        rows = []
        for patient_num, term_results in results.items():
            for term, found in term_results.items():
                rows.append({
                    'mrn':        patient_num,
                    'code':       '{}:{}'.format(output_concept_code, term.replace(' ', '_')),
                    'start-date': '1970-01-01 00:00:00',
                    'value':      '1' if found else '0',
                })

        if rows:
            df = pd.DataFrame(rows)
            self.send_facts(df)

        self.output = results
