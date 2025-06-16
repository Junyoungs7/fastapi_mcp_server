from mcp.server import Server
from mcp.server.fastmcp import FastMCP
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.routing import Mount, Route
from starlette.responses import Response


from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import services.customer_service as customer_service

load_dotenv()

mcp = FastMCP("fastapi-mcp-server")

@mcp.tool()
async def get_customers(name: str, phone: str = None, email: str = None):
    """Retrieve customer information from the database.

    Args:
        name (str): The name of the customer.
        phone (str, optional): The phone number of the customer. Defaults to None.
        email (str, optional): The email address of the customer. Defaults to None.

    Returns:
        dict: A dictionary containing customer information.
    """
    return await customer_service.search_db(name=name, phone=phone, email=email)


def create_starlette_app(mcp_server: Server, *, debug: bool = False) -> Starlette:
    """Create a Starlette application that can server the provied mcp server with SSE."""
    sse = SseServerTransport("/messages/")

    async def handle_sse(request: Request) -> Response:
        async with sse.connect_sse(
            request.scope,
            request.receive,
            request._send,
        ) as (read_stream, write_stream):
            await mcp_server.run(
                read_stream,
                write_stream,
                mcp_server.create_initialization_options(),
            )
        return Response()

    return Starlette(
        debug=debug,
        routes=[
            Route("/sse", endpoint=handle_sse),
            Mount("/messages/", app=sse.handle_post_message),
        ],
    )

if __name__ == "__main__":
    # stdio는 표준 입력/출력 스트림을 사용하여 MCP 서버를 실행합니다.
    # 이 모드에서는 MCP 서버가 표준 입력을 통해 요청을 받고, 표준 출력을 통해 응답을 반환합니다.
    # 이는 주로 개발 및 테스트 환경에서 사용됩니다.
    # 만약 각각 서버를 실행하고 싶다면, 아래와 같이 transport를 변경할 수 있습니다.
    # mcp.run(transport="sse")  # SSE (Server-Sent Events) 모드
    # print("Starting FastMCP server...")
    # mcp.run(transport="sse")
    # import uvicorn
    # uvicorn.run(app, host="0.0.0.0", port=8001)
    mcp_server = mcp._mcp_server
    
    import argparse
    import uvicorn
    
    parser = argparse.ArgumentParser(description="Run the FastMCP server.")
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()
    
    starlette_app = create_starlette_app(mcp_server, debug=True)

    uvicorn.run(starlette_app, host=args.host, port=args.port)