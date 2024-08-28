import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging

from app import endpoints

app = FastAPI()
app.include_router(endpoints.router)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):

    logging.exception("Unhandled server extencion")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)