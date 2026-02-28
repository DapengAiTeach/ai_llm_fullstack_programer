from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="用户登录服务")

# 内存存储用户信息
users_db = {}


class User(BaseModel):
    username: str
    password: str


# 导入并注册路由
from web import register

app.include_router(register.router)


@app.post("/login")
def login(user: User):
    """用户登录"""
    if user.username not in users_db:
        raise HTTPException(status_code=400, detail="用户名或密码错误")
    
    if users_db[user.username] != user.password:
        raise HTTPException(status_code=400, detail="用户名或密码错误")
    
    return {"message": "登录成功", "username": user.username}


@app.get("/")
def root():
    return {"message": "用户登录服务"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
