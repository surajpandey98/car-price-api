from fastapi import FastAPI
from fastapi.responses import JSONResponse
from schema import CarFeatures,PredictionResponse
from model import predict_price,load_artifacts
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app:FastAPI):
    load_artifacts
    yield

app=FastAPI(lifespan=lifespan,title="Car Price Prediction API",version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_mwthods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def test():
    return JSONResponse(
        status_code=200,
        content={
            "success":True
            ,"message":"This is test route"
        }
    )

@app.post("/predict",response_model=PredictionResponse)
def predict(features:CarFeatures):
    price=predict_price(features.model_dump())
    return PredictionResponse(prediction_price=price)