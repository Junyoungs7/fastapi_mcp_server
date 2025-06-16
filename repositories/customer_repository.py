from dbconnection.diablo import db_manager as db


async def fetch_user_info(cus_name: str):
    query = "SELECT TOP 1 CUS_NO, CUS_NAME, BIRTH_DATE FROM dbo.CUS_CUSTOMER_damo WHERE CUS_NAME = ?"
    results = db.execute_query(query, (cus_name,))
    return results

