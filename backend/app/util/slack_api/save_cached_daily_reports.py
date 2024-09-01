from app.services.redis_client import redis_client
from sqlalchemy.orm import Session
from app.db.models import DailyReport
import logging
from dotenv import load_dotenv
import os

# 環境変数の読み込み
load_dotenv()

# ロギングの設定
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 日報投稿のバッチ処理を行う関数
def save_cached_daily_reports_to_db(db: Session):
    keys = redis_client.keys("daily_report:*")
    for key in keys:
        ts = key.split(":")[1]
        user_id = redis_client.hget(key, "user_id").decode("utf-8")
        text = redis_client.hget(key, "text").decode("utf-8")

        # 既存のメッセージをチェック
        existing_message = db.query(DailyReport).filter_by(ts=ts).first()
        if existing_message:
            # メッセージが存在する場合、内容を更新
            existing_message.text = text
            logger.debug(f"◆◆キャッシュからメッセージを更新しました: ts={ts}, user_id={user_id}")
        else:
            # メッセージが存在しない場合、新規に追加
            message_record = DailyReport(ts=ts, slack_user_id=user_id, text=text)
            db.add(message_record)
            logger.debug(f"◆◆キャッシュからメッセージを追加しました: ts={ts}, user_id={user_id}")

    # コミットして変更を保存
    db.commit()

    # Redisキャッシュを削除
    for key in keys:
        redis_client.delete(key)
