from fastapi import FastAPI
from web import register, login

app = FastAPI(title="用户登录服务")
app.include_router(register.router)
app.include_router(login.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
