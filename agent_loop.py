"""
一个agent loop处理用户的一次query
"""

from brain import call_agent_brain
from tools import *

def main_loop(history, user_input):
    while True:
        thought = call_agent_brain(history, user_input)
        action, response = parse(thought)
        if action == "FINISH":
            return response
        if action == "tool_bash":
            observation = call_tool_bash(cmd)
        elif action == "tool_read_file":
            observation = call_tool_read_file(fpath)
        history += [action, observation]


if __name__ == "__main__":
    main_loop([], "who are you?")