"""
LLM 调用层：封装 DeepSeek Chat Completions 接口。

文档：https://api-docs.deepseek.com/zh-cn/
- base_url: https://api.deepseek.com（OpenAI 兼容格式）
- 认证:    Authorization: Bearer <DS_API_KEY>
- 模型:    deepseek-flash（推荐，1M 上下文，最大输出 384K）
           deepseek-v4-pro（更强更贵）

只依赖标准库 + python-dotenv，不需要安装 openai SDK。
"""

import json
import os
import time
import urllib.error
import urllib.request

from dotenv import load_dotenv

load_dotenv()  # 从当前目录或父目录找 .env，写进 os.environ
api_key = os.environ["DS_API_KEY"]

BASE_URL = os.environ.get("DS_BASE_URL", "https://api.deepseek.com")
DEFAULT_MODEL = os.environ.get("DS_MODEL", "deepseek-flash")
CHAT_URL = f"{BASE_URL.rstrip('/')}/chat/completions"


class LLMError(RuntimeError):
    """API 调用失败（非 2xx、网络错误、返回体不合法）。"""


def chat(
    messages,
    model=DEFAULT_MODEL,
    temperature=0.7,
    max_tokens=4096,
    timeout=120,
    retries=3,
    **extra,
):
    """
    发送一组 messages，返回 assistant 的回复文本。

    messages: [{"role": "system"|"user"|"assistant", "content": "..."}, ...]
    extra:    透传给接口的其他字段，如 response_format={"type": "json_object"}、
              stop=[...]、tools=[...] 等。
    """
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": False,
        **extra,
    }
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    last_err = None
    for attempt in range(1, retries + 1):
        req = urllib.request.Request(CHAT_URL, data=body, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"]
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", errors="replace")
            last_err = LLMError(f"HTTP {e.code}: {detail}")
            # 4xx（鉴权、参数错误、余额不足）重试没有意义，直接抛
            if 400 <= e.code < 500 and e.code != 429:
                raise last_err
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, KeyError) as e:
            last_err = LLMError(f"{type(e).__name__}: {e}")

        if attempt < retries:
            time.sleep(2 ** (attempt - 1))  # 1s, 2s, ...

    raise last_err


def call_llm(prompt, system=None, **kwargs):
    """
    单轮调用：给一段 prompt，返回回复文本。
    system 可选，作为 system message 放在最前面。
    """
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    return chat(messages, **kwargs)


if __name__ == "__main__":
    print(call_llm("用一句话介绍你自己。"))
