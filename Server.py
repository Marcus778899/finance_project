import uvicorn
from src.app import app
from src.setting import SERVER_INFO

if __name__ == "__main__":
    uvicorn.run("Server:app",host=SERVER_INFO['url'],port=SERVER_INFO['port'],reload=False)