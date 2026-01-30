# app/auth.py
import os
import requests
from jose import jwt, JWTError

SUPABASE_PROJECT_URL = os.getenv("SUPABASE_PROJECT_URL")
JWKS_URL = f"{SUPABASE_PROJECT_URL}/auth/v1/keys"


def get_jwks():
    resp = requests.get(JWKS_URL, timeout=5)
    resp.raise_for_status()
    return resp.json()


def verify_supabase_token(token: str) -> dict | None:
    try:
        jwks = get_jwks()
        header = jwt.get_unverified_header(token)

        key = next(
            k for k in jwks["keys"] if k["kid"] == header["kid"]
        )

        payload = jwt.decode(
            token,
            key,
            algorithms=["ES256", "RS256"],
            audience="authenticated",
            issuer=SUPABASE_PROJECT_URL,
        )

        return payload

    except (JWTError, StopIteration, Exception):
        return None
