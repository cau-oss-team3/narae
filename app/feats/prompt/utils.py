import re
from typing import Dict, Any


def inject_variables(prompt: str, variables: Dict[str, Any]) -> str:
    for key, value in variables.items():
        placeholder = f"{{{{{key}}}}}"
        prompt = prompt.replace(placeholder, str(value))
    return prompt


def extract_tagged_sections(text: str) -> Dict[str, str]:
    tags = re.findall(r"<(.*?)>", text)
    sections = {}
    for tag in tags:
        pattern = f"<{tag}>(.*?)</{tag}>"
        match = re.search(pattern, text, re.DOTALL)
        if match:
            sections[tag] = match.group(1).strip()
    return sections
