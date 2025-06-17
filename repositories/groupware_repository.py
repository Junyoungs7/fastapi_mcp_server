from dbconnection.diablo import db_manager as db
from typing import Optional

async def select_meeting_room(floor: int, start_date: str, end_date: str, room_name: Optional[str] = None):
    query = """
        SELECT CMS.SCH_DATE, CMS.ROOM_NAME, CMS.START_TIME, CMS.END_TIME, CMS.MEET_TYPE, CMS.SUBJECT, CMS.TEAM_NAME, CMS.EMP_NAME
        FROM COM_MEETROOM_SCHEDULE CMS
        WHERE CMS.SCH_DATE BETWEEN ? AND ?
        AND CMS.DEL_YN IS NULL
    """
    params = [start_date, end_date]

    if room_name:
        query += " AND CMS.ROOM_NAME = ?"
        params.append(room_name)

    query += " AND CMS.ROOM_FLOOR = ?"
    params.append(str(floor))

    query += " ORDER BY CMS.SCH_DATE, CMS.START_TIME, CMS.ROOM_NAME"

    results = db.execute_query(query, tuple(params))
    return results

async def insert_meeting_room(resv_type: str, room_name: str, room_floor: str, meet_type: str
                            , subject: str, sch_date: str, sch_end_date: str, start_time: str, end_time: str, team_name: str, emp_code: str, emp_name: str):
    query = """
        EXEC USP_GW_MEET_INSERT_SCHEDULE ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
    """
    params = (resv_type, room_name, room_floor, meet_type, subject, sch_date, sch_end_date, start_time, end_time, team_name, emp_code, emp_name)
    result = db.execute_query(query, params)
    

    if result == "중복":
        result = "이미 예약된 시간입니다."
    else:
        result = "예약이 완료되었습니다."

    return result

async def update_meeting_room(seq_no: str, resv_type: str, room_name: str, room_floor: str, meet_type: str, subject: str,
                            sch_date: str, sch_end_date: str, start_time: str, end_time: str,
                            team_name: str,  emp_code: str, emp_name: str):
    query = """
        EXEC USP_GW_MEET_UPDATE_SCHEDULE ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
    """
    params = (seq_no, resv_type, room_name, room_floor, meet_type, subject, sch_date, sch_end_date, start_time, end_time, team_name, emp_code, emp_name)
    result = db.execute_query(query, params)

    if result == "중복":
        result = "이미 예약된 시간입니다."
    else:
        result = "예약이 수정되었습니다."

    return result