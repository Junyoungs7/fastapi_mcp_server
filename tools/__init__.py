import logging
import traceback
from functools import wraps

logger = logging.getLogger("mcp_tools")
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


def mcp_safe_tool(func):
    """Decorator to handle exceptions in MCP tools and log them."""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            logger.info(f"Executing tool: {func.__name__} with args: {args}, kwargs: {kwargs}")
            result = await func(*args, **kwargs)
            logger.info(f"Tool {func.__name__} executed successfully.")
            return result
        except Exception as e:
            logger.error(f"Error in tool {func.__name__}: {e}")
            logger.debug(traceback.format_exc())
            return {
                "error": str(e),
                "message": "도구 실행 중 오류가 발생했습니다."
            }

    return wrapper