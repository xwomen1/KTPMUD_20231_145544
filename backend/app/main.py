from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import apirouter


#tu dong tao db
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(router=apirouter.router, prefix="/api")

