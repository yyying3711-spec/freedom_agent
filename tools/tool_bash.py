import subprocess

def run_bash(command: str, timeout: int = 30) -> str:
    try:
        r = subprocess.run(
            ["bash", "-lc", command],
            capture_output=True, text=True,
            timeout=timeout, cwd="/workspace"
        )
        out = r.stdout[-8000:]  # 截断，别把 10 万行日志塞回上下文
        if r.returncode != 0:
            out += f"\n[exit {r.returncode}] {r.stderr[-2000:]}"
        return out
    except subprocess.TimeoutExpired:
        return f"[timeout after {timeout}s]"