
import repositories.customer_repository as customer_repo
import utils.db_util as utils
from typing import Optional

async def cus_info_search_db(name: str, phone: Optional[str] = None, email: Optional[str] = None):
    customer_info = await customer_repo.fetch_user_info(name)
    if not customer_info:
        raise ValueError("해당 고객 정보를 찾을 수 없습니다.")
    customer_info = utils.decode_bytes_in_dict(customer_info)
    return customer_info