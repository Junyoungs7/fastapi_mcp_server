import pyodbc
from fastapi import HTTPException
from dotenv import load_dotenv
from configs.db_settings import SERVER, DATABASE, UID, PWD

load_dotenv()


class DBConnectionManager:
    def __init__(self, dsn: str):
        self.dsn = dsn
        self.connection = None

    def connect(self):
        if self.connection is None:
            try:
                self.connection = pyodbc.connect(self.dsn)
                print("✅ DB 연결됨")
            except pyodbc.Error as e:
                raise HTTPException(status_code=500, detail=f"DB 연결 실패: {str(e)}")

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            print("❌ DB 연결 종료됨")

    def execute_query(self, query: str, params: tuple = ()):
        if self.connection is None:
            raise HTTPException(status_code=500, detail="DB 연결이 되어 있지 않습니다.")
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            
            # COMMIT 필요 시
            self.connection.commit()

            # 결과가 있는 경우만 fetch 처리
            if cursor.description is not None:
                columns = [column[0] for column in cursor.description]
                rows = cursor.fetchall()
                return [dict(zip(columns, row)) for row in rows] if rows else []

            return None  # 혹은 "성공" 등 필요에 맞게
        except pyodbc.Error as e:
            raise HTTPException(status_code=500, detail=f"쿼리 실행 실패: {str(e)}")

    def execute_query_with_columns(self, query: str, params: tuple = ()):
        if self.connection is None:
            raise HTTPException(status_code=500, detail="DB 연결이 되어 있지 않습니다.")
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        cursor.commit()
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        return [dict(zip(columns, row)) for row in rows]


dsn = (
    "Driver={ODBC Driver 17 for SQL Server};"
    f"Server={SERVER};"
    f"Database={DATABASE};"
    f"UID={UID};"
    f"PWD={PWD};"
)

db_manager = DBConnectionManager(dsn)


def init_db_connection():
    try:
        db_manager.connect()
        # print("✅ Database connection established successfully")
    except Exception as e:
        print(f"❌ Failed to connect to the database: {e}")


def close_db_connection():
    try:
        db_manager.close()
        # print("❌ Database connection closed successfully")
    except Exception as e:
        print(f"❌ Failed to close the database connection: {e}")
