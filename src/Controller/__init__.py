from .ImageController import image_router
from .ScarpingController import scraping_router
from .BullshitController import bullshit_router

all_controller = [image_router, scraping_router,bullshit_router]