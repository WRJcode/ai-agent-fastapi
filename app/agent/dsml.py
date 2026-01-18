# app/agent/dsml.py
import re

def extract_query_from_dsml(content: str) -> str:
    match = re.search(r"<｜DSML｜parameter name=\"query\".*?>(.*?)</", content)
    return match.group(1) if match else ""
