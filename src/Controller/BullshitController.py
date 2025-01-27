import json
from fastapi import APIRouter,HTTPException,status
from pydantic import BaseModel
from ..Bullshit.helath_soul import BullShit
from ..setting import send_warn, send_info

bullshit_router = APIRouter(prefix="/bullshit",tags=['bullshit'])

class RequestBody(BaseModel):
    topic: str
    content_length: int

@bullshit_router.post("")
async def bullshit_generate(request_body: RequestBody):
    data = request_body.model_dump()
    topic = data['topic']
    content_length = data['content_length']
    action = BullShit()
    try:
        str_gen = action.generate(topic,content_length)
        send_info(f"Topic <{topic}> create sucessfully")
        response={
            "content":str_gen,
            "status_code": status.HTTP_200_OK
        }
        return response
    
    except Exception as e:
        send_warn(str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexception error occured"
        )
