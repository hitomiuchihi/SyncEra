import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from app.util.summary.get_all_saved_summarize_history import get_all_saved_summary_reports
from app.db.models import SummarizeHistory
import json

# テストデータ
MOCK_SLACK_USER_ID = "mock_user"
MOCK_SUMMARY_REPORTS = [
    {"id": 1, "slack_user_id": MOCK_SLACK_USER_ID, "summary": "Summary 1", "created_at": "2023-01-01T00:00:00"},
    {"id": 2, "slack_user_id": MOCK_SLACK_USER_ID, "summary": "Summary 2", "created_at": "2023-01-02T00:00:00"}
]

@pytest.fixture
def mock_redis_client():
    with patch("app.services.redis_client.redis_client") as mock_redis:
        yield mock_redis

@pytest.fixture
def mock_db():
    with patch("app.db.database.get_db") as mock_db:
        yield mock_db

def test_get_all_saved_summary_reports_cache_hit(mock_redis_client, mock_db):
    # Mock Redis to return cached data
    mock_redis_client.get.return_value = json.dumps(MOCK_SUMMARY_REPORTS)
    
    # Call function
    result = get_all_saved_summary_reports(MOCK_SLACK_USER_ID, mock_db)
    
    # Assertions
    assert result == MOCK_SUMMARY_REPORTS
    mock_redis_client.get.assert_called_once_with(f'summary_reports:{MOCK_SLACK_USER_ID}')

# def test_get_all_saved_summary_reports_db_query(mock_redis_client, mock_db):
#     # Mock Redis to return None (cache miss)
#     mock_redis_client.get.return_value = None

#     # Mock DB query
#     mock_session = MagicMock()
#     mock_db.return_value = mock_session
#     mock_session.query.return_value.filter.return_value.order_by.return_value.all.return_value = [
#         SummarizeHistory(**report) for report in MOCK_SUMMARY_REPORTS
#     ]
    
#     # Call function
#     result = get_all_saved_summary_reports(MOCK_SLACK_USER_ID, mock_db)
    
#     # Assertions
#     assert result == MOCK_SUMMARY_REPORTS
#     mock_redis_client.set.assert_called_once_with(f'summary_reports:{MOCK_SLACK_USER_ID}', json.dumps(MOCK_SUMMARY_REPORTS), ex=43200)
def test_get_all_saved_summary_reports_db_query(mock_redis_client, mock_db):
    # Mock Redis to return None (cache miss)
    mock_redis_client.get.return_value = None

    # Mock DB query
    mock_session = MagicMock()
    mock_db.return_value = mock_session
    mock_session.query.return_value.filter.return_value.order_by.return_value.all.return_value = [
        SummarizeHistory(**report) for report in MOCK_SUMMARY_REPORTS
    ]

    # Call function
    result = get_all_saved_summary_reports(MOCK_SLACK_USER_ID, mock_db)
    
    # Assertions
    assert result == MOCK_SUMMARY_REPORTS

def test_get_all_saved_summary_reports_no_data(mock_redis_client, mock_db):
    # Mock Redis to return None (cache miss)
    mock_redis_client.get.return_value = None
    
    # Mock DB query to return no data
    mock_session = MagicMock()
    mock_db.return_value = mock_session
    mock_session.query.return_value.filter.return_value.order_by.return_value.all.return_value = []
    
    # Call function and expect HTTPException
    with pytest.raises(HTTPException) as excinfo:
        get_all_saved_summary_reports(MOCK_SLACK_USER_ID, mock_db)
    
    # Assertions
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "このユーザーのサマリーデータが見つかりません"

def test_get_all_saved_summary_reports_redis_error(mock_redis_client, mock_db):
    # Mock Redis to raise an exception
    mock_redis_client.get.side_effect = Exception("Redis error")
    
    # Call function and expect HTTPException
    with pytest.raises(HTTPException) as excinfo:
        get_all_saved_summary_reports(MOCK_SLACK_USER_ID, mock_db)
    
    # Assertions
    assert excinfo.value.status_code == 500
    assert "Redis error" in str(excinfo.value.detail)
