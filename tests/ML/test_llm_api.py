from unittest.mock import patch

from flask import Flask, request

from i2b2_cdi.ML.llm_API import run_llm


def test_run_llm_calls_engine_and_returns_success():
    app = Flask(__name__)

    with app.test_request_context('/etl/llm_run', method='POST', json={'jobId': 7}):
        with patch('i2b2_cdi.ML.llm_API.llmEngine') as MockEngine:
            mock_engine = MockEngine.return_value
            response = run_llm(request)

    assert response.status_code == 200
    mock_engine.run.assert_called_once()
    mock_engine.save_output.assert_called_once()
