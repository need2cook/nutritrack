import hmac, hashlib, json, time
from urllib.parse import parse_qsl, unquote

from fastapi.exceptions import HTTPException


class InitDataError(Exception): ...

# ТЕСТ: max_age_sec сменить на 3600 после тестов
def parse_and_verify_init_data(init_data: str, bot_token: str, *, max_age_sec: int = 3600000) -> dict:
    if not init_data:
        raise InitDataError("Empty initData")
    
    data = dict(parse_qsl(unquote(init_data)))
    
    if 'hash' not in data:
        raise InitDataError("Missing hash")
    
    received_hash = data.pop('hash')
    
    data_check_string = '\n'.join([f"{k}={v}" for k, v in sorted(data.items())])
    
    secret_key = hmac.new(
        key=b"WebAppData",
        msg=bot_token.encode(),
        digestmod=hashlib.sha256
    ).digest()
    
    calculated_hash = hmac.new(
        key=secret_key,
        msg=data_check_string.encode(),
        digestmod=hashlib.sha256
    ).hexdigest()
    
    if not hmac.compare_digest(calculated_hash, received_hash):
        raise InitDataError("Invalid hash initData")
    
    try:
        auth_date = int(data.get("auth_date", "0"))
    except ValueError:
        raise InitDataError("Bad 'auth_date'")
    if auth_date == 0 or (time.time() - auth_date) > max_age_sec:
        raise InitDataError("initData expired")
    
    for k in ("user", "chat", "receiver"):
        if k in data:
            data[k] = json.loads(data[k])
    return data
        
