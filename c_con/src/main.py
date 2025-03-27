import hashlib
import time
import logging

from datetime import datetime
import cv2

from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


import uvicorn
# from database.data_controller import DatabaseController
# ------------------------------------------------------------------------------
# user routing suprise
# ------------------------------------------------------------------------------
from src.api.user_api.user import user_router

app.include_router(user_router, tags=["/api/users"])


# ------------------------------------------------------------------------------
# product routing suprise
# ------------------------------------------------------------------------------


from src.api.product_api.product_api import product_router

app.include_router(product_router, tags=["api/products"])

# ------------------------------------------------------------------------------
# user product interaction routing suprise
# ------------------------------------------------------------------------------
# from src.api.user_product_Interaction_api import user_product_router

# app.include_router(user_product_router, tags=["api/user_product_interaction"])
# ------------------------------------------------------------------------------
# main routing 
# ------------------------------------------------------------------------------


origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/api/status")
def health():
    
    return {"status": "alive", "code": 200}

@app.websocket("/ws/status")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        await websocket.send_json({"isAlive": True})
        data = await websocket.receive_json()
        data = data.get("isAlive", False)









if __name__ == "__main__":


    uvicorn.run(app, host="127.0.0.1", port=5001)
