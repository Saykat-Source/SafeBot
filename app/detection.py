import re

# Example lists (expand as needed)
BIAS_KEYWORDS = ["always", "never", "men are", "women are", "race", "religion"]
THREAT_PATTERNS = [r"\{.*?\}", r"\[.*?\]", r"(?i)password", r"(?i)secret"]

def detect_bias(text):
    for keyword in BIAS_KEYWORDS:
        if keyword.lower() in text.lower():
            return True, f"Bias detected: '{keyword}'"
    return False, ""

def detect_threat(text):
    for pattern in THREAT_PATTERNS:
        if re.search(pattern, text):
            return True, f"Threat pattern detected: '{pattern}'"
    return False, ""

def analyze_output(text):
    bias, bias_msg = detect_bias(text)
    threat, threat_msg = detect_threat(text)
    messages = []
    if bias:
        messages.append(bias_msg)
    if threat:
        messages.append(threat_msg)
    return messages
