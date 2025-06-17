import repositories.groupware_repository as groupware_repo
import utils.db_util as db_utils
import utils.date_util as date_utils
from typing import Optional

async def select_meeting_room(floor: int, start_date: Optional[str] = None, end_date: Optional[str] = None, room_name: Optional[str] = None):
    if start_date is None:
        start_date = date_utils.get_today_string()
    if end_date is None:
        end_date = date_utils.get_today_string()
    
    meeting_room = await groupware_repo.select_meeting_room(floor=floor, start_date=start_date, end_date=end_date, room_name=room_name)
    if not meeting_room:
        raise ValueError("해당 회의실 정보를 찾을 수 없습니다.")
    meeting_room = db_utils.decode_bytes_in_dict(meeting_room)
    return meeting_room

async def insert_meeting_room(room_name: str, room_floor: str, start_time: str, end_time: str, team_name: str, emp_code: str, emp_name: str,
                            meet_type: str = "내부회의", subject: str = "내부 회의", sch_date: Optional[str] = None, sch_end_date: Optional[str] = None):
    
    sch_date = sch_date or date_utils.get_today_string()
    sch_end_date = sch_end_date or sch_date
    
    if sch_date < date_utils.get_today_string():
        sch_date = date_utils.get_today_string()
    if sch_end_date < sch_date:
        sch_end_date = sch_date
        
    

    result = await groupware_repo.insert_meeting_room(resv_type="신규", room_name=room_name, room_floor=room_floor, meet_type=meet_type
                                            , subject=subject, sch_date=sch_date, sch_end_date=sch_end_date, start_time=start_time
                                            , end_time=end_time, team_name=team_name, emp_code=emp_code, emp_name=emp_name)
    return result


async def update_meeting_room():
    ...
    
async def delete_meeting_room():
    ...