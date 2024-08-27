from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from .stock_image import draw_stock_history
from . import logger

app = FastAPI(
    description="stock history picture",
    title="stock history picture",
    version="0.0.1",
    docs_url="/"
)

# setting CORS
origins = [
    "http://localhost"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/image")
def get_img(stock_id: str, condition: str = None , limit: int = 200):

    logger.info(f"""
                
stock_id: {stock_id}
condition: {condition}
limit: {limit}
"""
    )

    img_buf = draw_stock_history(stock_id, limit, condition)

    headers = {'Content-Disposition': 'inline; filename="out.png"'}
    content = img_buf.getvalue()

    img_buf.close()
    logger.info("Buffer close")
    
    return Response(content, headers=headers, media_type='image/png')