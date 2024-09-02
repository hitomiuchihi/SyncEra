import logging
import os
from dotenv import load_dotenv
from app.db.models import Employee
from app.db.database import get_db

load_dotenv()

log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 特定の従業員の情報を取得する
def get_employee_info(slack_user_id: str):
    logger.debug(f"◆{slack_user_id}の情報を取得します")
    # データベースからuser情報を取得してくる
    db = get_db()
    try:
        target_employee_info = db.query(Employee).filter(Employee.slack_user_id == slack_user_id).all()
        logger.debug(f"◆DBから指定ユーザーの情報を取得できました。{target_employee_info}")
        return target_employee_info
    except Exception:
        logger.error(f"◆指定ユーザーの情報を取得中にエラーが発生しました。: {Exception}")
        return[]
    finally:
        db.close()    

# 取得したデータを通常の文字列に変換する必要がある場合は以下の処理を加える。
def compile_target_employee_info(slack_user_id: str):
    pre_target_employee_info = get_employee_info(slack_user_id)

    # 会話履歴を文字列に変換
    if not pre_target_employee_info:
        logger.info("◆文字列に変換しようとしているユーザー情報が見つかりません。")
        compiled_target_employee_info = "指定されたユーザーの情報がありません。"
    else:
        compiled_target_employee_info = "必要に応じてここに出力形式を整える処理を追加する"
        logger.debug(f"◆指定ユーザーの情報を読解可能な文字列に変換しました。")
    
    return compiled_target_employee_info
