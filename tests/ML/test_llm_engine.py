"""Unit tests for llmEngine and llmHelper (no live DB or vLLM required)."""
import json
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from i2b2_cdi.ML.llmHelper import _build_prompt, extract_presence, get_notes


# ---------------------------------------------------------------------------
# llmHelper.get_notes
# ---------------------------------------------------------------------------

def test_get_notes_returns_records():
    mock_df = pd.DataFrame([
        {'patient_num': 1, 'encounter_num': 10, 'note_text': 'Patient has HbA1c elevated.', 'start_date': '2023-01-01'},
        {'patient_num': 2, 'encounter_num': 20, 'note_text': 'No medications noted.', 'start_date': '2023-02-01'},
    ])

    with patch('i2b2_cdi.ML.llmHelper.I2b2crcDataSource') as MockDS, \
         patch('i2b2_cdi.ML.llmHelper.getDataFrameInChunksUsingCursor', return_value=mock_df):
        MockDS.return_value.__enter__ = MagicMock(return_value=MagicMock())
        MockDS.return_value.__exit__ = MagicMock(return_value=False)

        config = MagicMock()
        notes = get_notes(config, '/Notes/Clinical/')

    assert len(notes) == 2
    assert notes[0]['patient_num'] == 1
    assert 'HbA1c' in notes[0]['note_text']


def test_get_notes_returns_empty_on_error():
    with patch('i2b2_cdi.ML.llmHelper.I2b2crcDataSource') as MockDS, \
         patch('i2b2_cdi.ML.llmHelper.getDataFrameInChunksUsingCursor', side_effect=Exception('DB error')):
        MockDS.return_value.__enter__ = MagicMock(return_value=MagicMock())
        MockDS.return_value.__exit__ = MagicMock(return_value=False)

        config = MagicMock()
        notes = get_notes(config, '/Notes/Clinical/')

    assert notes == []


# ---------------------------------------------------------------------------
# llmHelper.extract_presence
# ---------------------------------------------------------------------------

def _mock_vllm_response(answer_text):
    mock_resp = MagicMock()
    mock_resp.json.return_value = {
        'choices': [{'message': {'content': answer_text}}]
    }
    mock_resp.raise_for_status = MagicMock()
    return mock_resp


def test_extract_presence_found():
    notes = [{'patient_num': 1, 'encounter_num': 10, 'note_text': 'Patient takes metformin daily.', 'start_date': '2023-01-01'}]

    with patch('i2b2_cdi.ML.llmHelper.requests.post', return_value=_mock_vllm_response('yes')):
        results = extract_presence(notes, ['metformin'], 'http://localhost:8000', 'test-model')

    assert results[1]['metformin'] is True


def test_extract_presence_not_found():
    notes = [{'patient_num': 2, 'encounter_num': 20, 'note_text': 'No relevant medications.', 'start_date': '2023-02-01'}]

    with patch('i2b2_cdi.ML.llmHelper.requests.post', return_value=_mock_vllm_response('no')):
        results = extract_presence(notes, ['metformin'], 'http://localhost:8000', 'test-model')

    assert results[2]['metformin'] is False


def test_extract_presence_aggregates_across_notes():
    """Term found in second note → patient marked True."""
    notes = [
        {'patient_num': 1, 'encounter_num': 10, 'note_text': 'Nothing relevant.', 'start_date': '2023-01-01'},
        {'patient_num': 1, 'encounter_num': 11, 'note_text': 'HbA1c elevated.', 'start_date': '2023-03-01'},
    ]
    responses = [_mock_vllm_response('no'), _mock_vllm_response('yes')]

    with patch('i2b2_cdi.ML.llmHelper.requests.post', side_effect=responses):
        results = extract_presence(notes, ['HbA1c'], 'http://localhost:8000', 'test-model')

    assert results[1]['HbA1c'] is True


def test_extract_presence_skips_api_if_already_found():
    """Once a term is confirmed True for a patient, no further API calls for it."""
    notes = [
        {'patient_num': 1, 'encounter_num': 10, 'note_text': 'Has diabetes.', 'start_date': '2023-01-01'},
        {'patient_num': 1, 'encounter_num': 11, 'note_text': 'Follow-up visit.', 'start_date': '2023-03-01'},
    ]

    with patch('i2b2_cdi.ML.llmHelper.requests.post', return_value=_mock_vllm_response('yes')) as mock_post:
        results = extract_presence(notes, ['diabetes'], 'http://localhost:8000', 'test-model')

    # Only 1 call needed (second note skipped because already True)
    assert mock_post.call_count == 1
    assert results[1]['diabetes'] is True


def test_extract_presence_handles_api_error_gracefully():
    notes = [{'patient_num': 3, 'encounter_num': 30, 'note_text': 'Some note.', 'start_date': '2023-01-01'}]

    with patch('i2b2_cdi.ML.llmHelper.requests.post', side_effect=Exception('timeout')):
        results = extract_presence(notes, ['metformin'], 'http://localhost:8000', 'test-model')

    # Should not raise; term stays False
    assert results[3]['metformin'] is False


# ---------------------------------------------------------------------------
# llmHelper._build_prompt
# ---------------------------------------------------------------------------

def test_build_prompt_contains_term_and_note():
    prompt = _build_prompt('Patient has elevated HbA1c levels.', 'HbA1c')
    assert 'HbA1c' in prompt
    assert 'Patient has elevated HbA1c levels.' in prompt
    assert 'yes' in prompt.lower() or 'no' in prompt.lower()


# ---------------------------------------------------------------------------
# llmEngine.run (integration-level unit test)
# ---------------------------------------------------------------------------

def test_llm_engine_run_sends_facts():
    from i2b2_cdi.ML.llmEngine import llmEngine

    engine = llmEngine()

    mock_notes = [{'patient_num': 42, 'encounter_num': 1, 'note_text': 'Metformin prescribed.', 'start_date': '2023-01-01'}]
    mock_results = {42: {'metformin': True}}

    job_inputs = {
        'note_concept_path': '/Notes/Clinical/',
        'search_terms': ['metformin'],
        'output_concept_code': 'LLM:NLP:FOUND',
        'vllm_url': 'http://localhost:8000',
        'model': 'test-model',
    }

    with patch.object(engine, 'get_job_inputs', return_value=job_inputs), \
         patch('i2b2_cdi.ML.llmEngine.get_notes', return_value=mock_notes), \
         patch('i2b2_cdi.ML.llmEngine.extract_presence', return_value=mock_results), \
         patch.object(engine, 'send_facts') as mock_send, \
         patch('i2b2_cdi.ML.llmEngine.Config'):

        engine.run('job1', 'proj', None, 'LLM:NLP:FOUND', '/Notes/', None, 'llm')

    mock_send.assert_called_once()
    df_sent = mock_send.call_args[0][0]
    assert len(df_sent) == 1
    assert df_sent.iloc[0]['mrn'] == 42
    assert df_sent.iloc[0]['code'] == 'LLM:NLP:FOUND:metformin'
    assert df_sent.iloc[0]['value'] == '1'


def test_llm_engine_run_no_notes_skips_facts():
    from i2b2_cdi.ML.llmEngine import llmEngine

    engine = llmEngine()
    job_inputs = {
        'note_concept_path': '/Notes/Clinical/',
        'search_terms': ['metformin'],
        'output_concept_code': 'LLM:NLP:FOUND',
        'vllm_url': 'http://localhost:8000',
    }

    with patch.object(engine, 'get_job_inputs', return_value=job_inputs), \
         patch('i2b2_cdi.ML.llmEngine.get_notes', return_value=[]), \
         patch.object(engine, 'send_facts') as mock_send, \
         patch('i2b2_cdi.ML.llmEngine.Config'):

        engine.run('job2', 'proj', None, 'LLM:NLP:FOUND', '/Notes/', None, 'llm')

    mock_send.assert_not_called()
    assert engine.output == {}
