import json
from flask import jsonify, make_response, request
from loguru import logger

from i2b2_cdi.ML.llmEngine import llmEngine


def run_llm(request_obj=None):
    """Run the LLM extraction pipeline for a submitted job payload."""
    if request_obj is None:
        request_obj = request

    try:
        data = request_obj.get_json(silent=True) or {}
        job_id = data.get('jobId')
        project_name = data.get('projectName', 'Demo')
        job_input = data.get('input', {})
        concept_code = data.get('conceptCode')
        concept_path = data.get('conceptPath')
        node = data.get('node')
        job_type = data.get('jobType', 'llm')

        if not job_id:
            response = make_response(jsonify({'error': 'jobId is required'}))
            response.status_code = 400
            return response

        engine = llmEngine(jobId=job_id)
        engine.run(
            jobId=job_id,
            projectName=project_name,
            input=job_input,
            conceptCode=concept_code,
            conceptPath=concept_path,
            node=node,
            jobType=job_type,
        )
        engine.save_output()

        response = make_response(jsonify({'status': 'success', 'jobId': job_id}))
        response.status_code = 200
        return response

    except Exception as exc:
        logger.exception('LLM API failed: {}', exc)
        response = make_response(jsonify({'error': str(exc)}))
        response.status_code = 500
        return response
