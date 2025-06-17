from mcp.server import Server
from mcp.server.fastmcp import FastMCP
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.routing import Mount, Route
from starlette.responses import Response
from contextlib import asynccontextmanager

from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

from dbconnection.diablo import init_db_connection, close_db_connection
import tools.customer_tool as customer_tool
import tools.emp_tool as emp_tool
import tools.groupware_tool as groupware_tool

load_dotenv()

mcp = FastMCP("fastapi-mcp-server")

customer_tool.register_tools(mcp)
emp_tool.register_tools(mcp)
groupware_tool.register_tools(mcp)


# Initialize the database connection
@asynccontextmanager
async def lifespan(app: Starlette):
    print("📦 DB 연결 초기화 중...")
    init_db_connection()
    yield
    print("🧹 DB 연결 정리 중...")
    close_db_connection()



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
        lifespan=lifespan,
    )

if __name__ == "__main__":
    mcp_server = mcp._mcp_server
    
    import argparse
    import uvicorn
    
    parser = argparse.ArgumentParser(description="Run the FastMCP server.")
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()
    
    starlette_app = create_starlette_app(mcp_server, debug=True)
    

    uvicorn.run(starlette_app, host=args.host, port=args.port)