
"""
Agent大脑，它能感知：
1. 整体要求
2. 它能调用的工具
3. 上下文
4. 记忆[todo]
"""

from llm import call_llm

SP = """你是一个强大的代码智能体FREEDOM_AGENT. 根据用户输入和当前已知信息，给出下一步的执行动作。
【你可选的下一步动作】
1. tool_bash：用户要求尚未满足，需调用bash工具。
2. tool_read_file：用户要求尚未满足，需调用文件读取工具。
3. FINISH：用户要求已满足，返回最终回复。
【输出格式】
严格输出json格式，包含如下字段：
- action(str): 下一步需采取的动作，严格从以下三值中选择其一：`tool_bash | tool_read_file | FINISH`
- response(str): 简要的说明。
【用户需求】
{user_input}
【历史会话】
{history}
"""

def construct_prompt(history, user_input):
    return SP.format(user_input, history)

def call_agent_brain(history, user_input):
    prompt = construct_prompt(history, user_input)
    thought = call_llm(prompt)
    return thought