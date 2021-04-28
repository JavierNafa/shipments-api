from fastapi import FastAPI
from settings import fastapi_debug
from src.database.shipments import DatabaseShipments
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(debug=fastapi_debug,title='Shipments API')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['GET','POST','OPTIONS','PUT','DELETE'],
    allow_headers=['Origin','X-Requested-With','Content-Type','Accept','Authorization']
)

@app.on_event('startup')
async def startup():
    await DatabaseShipments.connect()

@app.on_event('shutdown')
async def shutdown():
    await DatabaseShipments.disconnect()
