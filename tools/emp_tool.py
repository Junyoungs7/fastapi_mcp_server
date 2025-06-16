from typing import Optional
import services.emp_service as employee_service
from tools import mcp_safe_tool

def register_tools(mcp):
    
    @mcp.tool()
    @mcp_safe_tool
    async def get_employee_info(name: str, phone: Optional[str] = None, email: Optional[str] = None):
        """Retrieve employee information from the database.

        Args:
            name (str): The name of the employee.
            phone (str, optional): The phone number of the employee. Defaults to None.
            email (str, optional): The email address of the employee. Defaults to None.

        Returns:
            dict: A dictionary containing employee information.
        """
        return await employee_service.emp_info_search_db(name=name, phone=phone, email=email)