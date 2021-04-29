from fastapi import FastAPI,Request,Depends
from src.routes import state,town,suburb,account
from settings import fastapi_debug
from jwt import InvalidTokenError
from src.middlewares.auth import verify_token
from sqlalchemy.exc import SQLAlchemyError
from fastapi.middleware.cors import CORSMiddleware
from src.database.shipments import DatabaseShipments
from src.middlewares.error_handler import ErrorHandler
from fastapi.exceptions import RequestValidationError,HTTPException,StarletteHTTPException

app = FastAPI(debug=bool(fastapi_debug),title='Shipments API')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['GET','POST','OPTIONS','PUT','DELETE'],
    allow_headers=['Origin','X-Requested-With','Content-Type','Accept','Authorization']
)

app.include_router(account.router)
app.include_router(state.router,dependencies=[Depends(verify_token)])
app.include_router(town.router,dependencies=[Depends(verify_token)])
app.include_router(suburb.router,dependencies=[Depends(verify_token)])

@app.on_event('startup')
async def startup():
    await DatabaseShipments.connect()

@app.on_event('shutdown')
async def shutdown():
    await DatabaseShipments.disconnect()

@app.exception_handler(InvalidTokenError)
async def token_error_handler(request,e):
    json_response = await ErrorHandler.handle_error(request,e)
    return json_response

@app.exception_handler(RequestValidationError)
async def validation_error_handler(request,e):
    json_response = await ErrorHandler.handle_error(request,e)
    return json_response

@app.exception_handler(SQLAlchemyError)
async def database_error_handler(request,e):
    json_response = await ErrorHandler.handle_error(request,e)
    return json_response

@app.exception_handler(StarletteHTTPException)
async def http_error_handler(request,e):
    json_response = await ErrorHandler.handle_error(request,e)
    return json_response