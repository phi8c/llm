from typing import List

def allowed_scopes(role: str) -> List[str]:
    if role == "admin":
        return ["admin", "hr", "staff", "public"]
    if role == "hr":
        return ["hr", "public"]
    if role == "staff":
        return ["staff", "public"]
    return ["public"]
