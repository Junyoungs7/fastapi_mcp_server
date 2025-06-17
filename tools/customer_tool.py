from typing import Optional
import services.customer_service as customer_service
from tools import mcp_safe_tool

def register_tools(mcp):
    
    @mcp.tool()
    @mcp_safe_tool
    async def get_customer_info(name: str, phone: Optional[str] = None, email: Optional[str] = None):
        """Retrieve customer information from the database.

        Args:
            name (str): The name of the customer.
            phone (str, optional): The phone number of the customer. Defaults to None.
            email (str, optional): The email address of the customer. Defaults to None.

        Returns:
            dict: A dictionary containing customer information.
        """
        return await customer_service.cus_info_search_db(name=name, phone=phone, email=email)