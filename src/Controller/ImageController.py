from fastapi import APIRouter, HTTPException,status, Response
from ..StockImage.draw_picture import StockImage
from ..setting import send_info

image_router = APIRouter(prefix="/image",tags=["images"])


@image_router.get("")
def get_img(stock_id: str, limit: int = 200):
    try:
        send_info(f"stock_id: {stock_id};limit: {limit}")

        action = StockImage(stock_id, limit)
        img_buf = action.draw_picture()

        headers = {'Content-Disposition': 'inline; filename="out.png"'}
        content = img_buf.getvalue()

        img_buf.close()
        send_info("Buffer close")

        return Response(
            content, 
            headers=headers, 
            media_type='image/png',
            status_code=status.HTTP_200_OK
            )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Draw Image Failed"
        )