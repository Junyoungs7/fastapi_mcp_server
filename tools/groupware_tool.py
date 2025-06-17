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
            floor (int): The floor number to search for meeting rooms.
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
                                room_name: str = "6-B회의실", room_floor: str = "6", team_name: str = "IT개발팀",
                                meet_type: str = "내부 회의", subject: str = "내부 회의", sch_date: Optional[str] = None, sch_end_date: Optional[str] = None):
        """
            Insert a meeting room reservation with the given details.

            This function reserves a meeting room based on provided information. If `sch_date` is not specified, the reservation will default to today's date. Both `sch_date` and `sch_end_date` must be in YYYY-MM-DD format. Required fields must be provided; if not, the assistant should ask for them again.

            Args:
                start_time (str): The reservation start time (e.g., "12:00"). **Required.**
                end_time (str): The reservation end time (e.g., "13:00"). **Required.**
                emp_code (str): The employee code of the person reserving the room. **Required.**
                emp_name (str): The employee name of the person reserving the room. **Required.**
                room_name (str): The meeting room name. Defaults to "6-B회의실".
                room_floor (str): The floor number of the meeting room. Defaults to "6".
                team_name (str): The name of the reserving team. Defaults to "IT개발팀".
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
    async def update_meeting_room():
        ...
    
    
    @mcp.tool()
    @mcp_safe_tool
    async def delete_meeting_room():
        ...