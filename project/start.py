import uvicorn
from config import get_settings

if __name__ == '__main__':
    settings = get_settings()
    uvicorn.run('app:create_app', factory=True, host=settings.HOST, port=settings.PORT)
