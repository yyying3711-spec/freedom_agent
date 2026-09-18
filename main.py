
"""
agent服务：
- 感知用户输入
- session管理
- agent loop调起
"""

from agent_loop import main_loop
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="FREEDOM_AGENT_SERVER")
history = []

class UserInput(BaseModel):
    content: str

@app.post("/work")
def create_item(user_input: UserInput):
    return main_loop(history, user_input)