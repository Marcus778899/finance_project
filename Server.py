import uvicorn
from api import Flaskapp

if __name__ == '__main__':
    uvicorn.run('Server:Flaskapp', host='127.0.0.1',port=8000, reload=True)