from fastapi import FastAPI
from core import db

app = FastAPI(title="用户登录服务")


# 导入并注册路由
from web import register, login, activate

app.include_router(register.router)
app.include_router(login.router)
app.include_router(activate.router)


@app.get("/")
def root():
    return {"message": "用户登录服务"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
