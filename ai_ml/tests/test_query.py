"""
Unit and integration tests for query and hybrid retrieval interface.
"""

import pytest
from ai_ml.interfaces.query_interface import query_knowledge


def test_query_knowledge_success():
    query_str = "What was the vibration issue with PUMP-101A?"
    res = query_knowledge(query_str)

    assert "answer" in res
    assert isinstance(res["answer"], str)
    assert "sources" in res
    assert "confidence" in res
    assert res["confidence"] > 0.0


def test_query_knowledge_empty_string():
    with pytest.raises(ValueError):
        query_knowledge("")
