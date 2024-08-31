import os
from dotenv import load_dotenv
import logging
from app.services.redis_client import redis_client
from sqlalchemy.orm import Session
from app.db.models import UserResponse

log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def store_user_response_temporarily(user_id: str, question_id: int, answer: str):
    logger.info(f"◆◆{user_id}のキャリアアンケートの回答をキャッシュに保存しました")
    redis_client.hset(f"user_response:{user_id}", question_id, answer)

def save_responses_to_db(user_id: str, db: Session):
    responses = redis_client.hgetall(f"user_response:{user_id}")
    for question_id, answer in responses.items():
        new_response = UserResponse(slack_user_id=user_id, question_id=question_id, answer=answer)
        db.add(new_response)
    db.commit()
    logger.info(f"◆◆{user_id}のキャリアアンケートの回答をデータベースに保存しました")
    redis_client.delete(f"user_response:{user_id}")
    logger.info(f"◆◆{user_id}のキャリアアンケートの回答をキャッシュから削除しました")
