from typing import Optional
import services.groupware_service as groupware_service
from tools import mcp_safe_tool

def register_tools(mcp):
    
    @mcp.tool()
    @mcp_safe_tool
    async def select_meeting_room(floor: int, start_date: Optional[str] = None, end_date: Optional[str] = None, room_name: Optional[str] = None):
        """
        Retrieve meeting room reservation information based on the specified floor and date range.

        Args:
            floor (int): The floor number to search for meeting rooms. e.g., 6, 11, 12 **Required.**
            start_date (Optional[str]): The start date for the reservation search in YYYY-MM-DD format. Defaults to today if not provided.
            end_date (Optional[str]): The end date for the reservation search in YYYY-MM-DD format. Defaults to today if not provided.
            room_name (Optional[str]): The name of the meeting room to filter by. If not provided, results include all rooms on the specified floor.

        Returns:
            list: A list of meeting room reservations. Each reservation is a dictionary with the following fields:
                - SCH_DATE (str): The reservation date in YYYY-MM-DD format.
                - ROOM_NAME (str): The name of the reserved meeting room.
                - START_TIME (str): The reservation start time (e.g., "09:00").
                - END_TIME (str): The reservation end time (e.g., "10:00").
                - MEET_TYPE (str): The type or purpose of the meeting (e.g., internal, client, etc.).
                - SUBJECT (str): The title or subject of the meeting.
                - TEAM_NAME (str): The team or department that booked the meeting room.
                - EMP_NAME (str): The name of the employee who made the reservation.

            The result represents the meeting room reservations scheduled on the specified floor and within the given date range.
        """
        return await groupware_service.select_meeting_room(floor=floor, start_date=start_date, end_date=end_date, room_name=room_name)
    
    @mcp.tool()
    @mcp_safe_tool
    async def insert_meeting_room(start_time: str, end_time: str, emp_code: str, emp_name: str,
                                room_name: str, room_floor: str, team_name: str,
                                sch_date: str, sch_end_date: str,
                                meet_type: str = "내부회의", subject: str = "내부 회의"):
        """
            Insert a meeting room reservation with the given details.

            This function reserves a meeting room based on provided information. If `sch_date` is not specified, the reservation will default to today's date. Both `sch_date` and `sch_end_date` must be in YYYY-MM-DD format. Required fields must be provided; if not, the assistant should ask for them again.

            Args:
                start_time (str): The reservation start time (e.g., "12:00"). **Required.**
                end_time (str): The reservation end time (e.g., "13:00"). **Required.**
                emp_code (str): The employee code of the person reserving the room. **Required.**
                emp_name (str): The employee name of the person reserving the room. **Required.**
                room_name (str): The meeting room name. If the word '회의실' is not in room_name, add it at the end. **Required.**
                room_floor (str): The floor number of the meeting room. **Required.**
                team_name (str): The name of the reserving team. **Required.**
                meet_type (str): The type of meeting. One of: "내부회의", "외부회의", or "고객상담".
                subject (str): The meeting subject or title. Defaults to "내부 회의".
                sch_date (Optional[str]): The start date of the reservation in YYYY-MM-DD format. If not provided, today's date will be used.
                sch_end_date (Optional[str]): The end date of the reservation in YYYY-MM-DD format. If not provided, it will default to the same value as `sch_date`.

            Returns:
                str: A message indicating whether the reservation was successful or if there was a conflict.

            Example output fields (in case of success):
                - "예약이 완료되었습니다."
                - "이미 예약된 시간입니다." (if time is already booked)

            Note:
                - Required parameters (`start_time`, `end_time`, `emp_code`, `emp_name`) must not be omitted.
                - The assistant should ensure valid time and date formats.
                - If user says "today" or "내일", it should be converted to the proper YYYY-MM-DD date string.
        """


        return await groupware_service.insert_meeting_room(
            room_name=room_name,
            room_floor=room_floor,
            start_time=start_time,
            end_time=end_time,
            team_name=team_name,
            emp_code=emp_code,
            emp_name=emp_name,
            meet_type=meet_type,
            subject=subject,
            sch_date=sch_date,
            sch_end_date=sch_end_date
        )
        
    @mcp.tool()
    @mcp_safe_tool
    async def update_meeting_room(seq_no: str, start_time: str, end_time: str,
                                room_name: str, room_floor: str,
                                team_name: str, sch_date: str, sch_end_date: str,
                                emp_code: str, emp_name: str,
                                meet_type: str = "내부회의",
                                subject: str = "내부 회의"):
        """
        Update an existing meeting room reservation identified by seq_no.
        Args:
            seq_no (str): 수정하려는 예약의 고유 식별자. 필수.
            start_time (Optional[str]): 변경할 시작 시간 "HH:MM".
            end_time (Optional[str]): 변경할 종료 시간 "HH:MM".
            room_name (Optional[str]): 변경할 회의실 이름.
            room_floor (Optional[str]): 변경할 층수.
            team_name (Optional[str]): 변경할 팀명.
            meet_type (Optional[str]): "내부회의", "외부회의", "고객상담".
            subject (Optional[str]): 변경할 회의 제목.
            sch_date (Optional[str]): 변경할 날짜 "YYYY-MM-DD".
            sch_end_date (Optional[str]): 변경할 종료 날짜 "YYYY-MM-DD".
        Returns:
            str: "수정이 완료되었습니다." 또는 오류/충돌 메시지.
        Note:
            - seq_no가 유효해야 하며, 충돌 확인이 필요함.
        """
        return await groupware_service.update_meeting_room(
            seq_no=seq_no,
            start_time=start_time,
            end_time=end_time,
            room_name=room_name,
            room_floor=room_floor,
            team_name=team_name,
            meet_type=meet_type,
            subject=subject,
            sch_date=sch_date,
            sch_end_date=sch_end_date,
            emp_code=emp_code,
            emp_name=emp_name
        )
    
    @mcp.tool()
    @mcp_safe_tool
    async def delete_meeting_room():
        ...