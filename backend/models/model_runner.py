import subprocess
import json
import shlex
from typing import Any

OLLAMA_MODEL = "phi3"

def call_ollama_cli(promt: str) -> str:
    cmd = ["ollama", "run", OLLAMA_MODEL]
    try:
        proc = subprocess.run(
            cmd, 
            input=promt.encode("utf-8"), 
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        out = proc.stdout.decode("utf-8", errors="ignore")

        lines = [line for line in out.splitlines() if line.strip() != f"{OLLAMA_MODEL}"]
        return "\n".join(lines).strip()

    except subprocess.CalledProcessError as e:
        print("OLLAMA CLI call failed: ", e.stderr.decode("utf-8"))
        return f"[OLLAMA-ERROR] {e.stderr.decode('utf-8')}"
    except Exception as e:
        return f"[OLLAMA-ERROR] {str(e)}"

def call_llm(prompt: str) -> str:
    return call_ollama_cli(prompt)

if __name__ == "__main__":
    test_prompt = "Explain free-space path loss formula."
    print(call_llm(test_prompt))