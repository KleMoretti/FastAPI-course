from fastapi import FastAPI
from starlette import status
from starlette.responses import RedirectResponse

import models
from database import engine
from routers import auth,todos,admin,users
from starlette.staticfiles import StaticFiles
app=FastAPI()

models.Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return RedirectResponse(url="/todo", status_code=status.HTTP_302_FOUND)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        app='main:app',
        host='127.0.0.1',
        port=8000,
        reload=True
    )