import uvicorn
from api.webapi import app

if __name__ == '__main__':
    uvicorn.run('api.webapi:app', host='127.0.0.1',port=8000, reload=True)