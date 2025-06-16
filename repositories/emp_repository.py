from dbconnection.diablo import db_manager as db


async def fetch_emp_info(emp_name: str):
    query = "SELECT EMP_CODE, KOR_NAME, EMAIL, BIRTH_DATE FROM dbo.EMP_MASTER_damo WHERE KOR_NAME LIKE ?"
    like_param = f"%{emp_name}%"
    results = db.execute_query(query, (like_param,))
    return results

