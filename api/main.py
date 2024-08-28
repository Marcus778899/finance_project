from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from .stock_image import StockImage
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
def get_img(stock_id: str, condition: str = None, limit: int = 200):
    try:
        logger.info(f"""
    stock_id: {stock_id}
    condition: {condition}
    limit: {limit}
    """
        )

        action = StockImage(stock_id, limit, condition)
        img_buf = action.draw_picture()

        headers = {'Content-Disposition': 'inline; filename="out.png"'}
        content = img_buf.getvalue()

        img_buf.close()
        logger.info("Buffer close")

        return Response(content, headers=headers, media_type='image/png')
    except Exception as e:
        logger.exception(e)
        return {"error": str(e)}