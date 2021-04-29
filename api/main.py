import uvicorn
from app import app
from settings import api_port

if __name__ == '__main__':
    uvicorn.run(app,host='0.0.0.0',port=int(api_port))