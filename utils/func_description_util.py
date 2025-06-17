def generate_mcp_docstring(tool_name: str, description: str, args: dict, return_fields: dict, note: str = "") -> str:
    docstring = f'"""\n{description}\n\nArgs:'
    for name, desc in args.items():
        docstring += f"\n    {name} ({desc['type']}): {desc['desc']}"
    docstring += "\n\nReturns:\n    list: A list of results. Each item is a dictionary with the following fields:"
    for field, meaning in return_fields.items():
        docstring += f"\n        - {field} ({meaning['type']}): {meaning['desc']}"
    if note:
        docstring += f"\n\n    {note}"
    docstring += '\n"""'
    return docstring

def temp_docstring():
    args = {
    "floor": {"type": "int", "desc": "The floor number to search for meeting rooms."},
    "start_date": {"type": "Optional[str]", "desc": "Start date in YYYY-MM-DD format. Defaults to today."},
    "end_date": {"type": "Optional[str]", "desc": "End date in YYYY-MM-DD format. Defaults to today."},
    "room_name": {"type": "Optional[str]", "desc": "Name of the meeting room to filter by."}
    }

    return_fields = {
        "SCH_DATE": {"type": "str", "desc": "The reservation date in YYYY-MM-DD format."},
        "ROOM_NAME": {"type": "str", "desc": "The name of the reserved meeting room."},
        "START_TIME": {"type": "str", "desc": "The start time of the reservation."},
        "END_TIME": {"type": "str", "desc": "The end time of the reservation."},
        "MEET_TYPE": {"type": "str", "desc": "The type or category of the meeting."},
        "SUBJECT": {"type": "str", "desc": "The subject or title of the meeting."},
        "TEAM_NAME": {"type": "str", "desc": "The team or department that reserved the room."},
        "EMP_NAME": {"type": "str", "desc": "The name of the employee who made the reservation."}
    }

    print(generate_mcp_docstring(
        tool_name="select_meeting_room",
        description="Retrieve meeting room reservation information based on the specified floor and date range.",
        args=args,
        return_fields=return_fields,
        note="The result represents meeting room reservations for the specified date range and floor."
    ))
