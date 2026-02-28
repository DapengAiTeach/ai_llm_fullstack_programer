from fastapi import FastAPI

app = FastAPI(title="用户登录服务")

# 内存存储用户信息
users_db = {}


# 导入并注册路由
from web import register, login

app.include_router(register.router)
app.include_router(login.router)


@app.get("/")
def root():
    return {"message": "用户登录服务"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
