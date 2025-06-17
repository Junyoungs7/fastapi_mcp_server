from datetime import datetime

def get_today_string() -> str:
    """오늘 날짜를 YYYY-MM-DD 형식의 문자열로 반환합니다."""
    return datetime.today().strftime("%Y-%m-%d")
