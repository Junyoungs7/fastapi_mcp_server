import repositories.emp_repository as emp_repo
import utils.db_util as utils
from typing import Optional

async def emp_info_search_db(name: str, emp_code: Optional[int] = None, phone: Optional[str] = None, email: Optional[str] = None):
    emp_info = await emp_repo.fetch_emp_info(name)
    if not emp_info:
        raise ValueError("해당 직원 정보를 찾을 수 없습니다.")
    emp_info = utils.decode_bytes_in_dict(emp_info)
    return emp_info