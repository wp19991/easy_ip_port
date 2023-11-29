# pip install fastapi "uvicorn[standard]"
import datetime
import os
import uvicorn

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return f"你好，现在的时间是{datetime.datetime.now()}"


@app.get("/file")
def file():
    return ','.join(os.listdir(r'C:\Users\wp\Desktop\计算机网络'))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081)
