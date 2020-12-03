import os

from dotenv import load_dotenv
from fastapi import HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader

load_dotenv()
api_key_header_auth = APIKeyHeader(name='Authorization', auto_error=True)


async def get_api_key(api_key_header: str = Security(api_key_header_auth)):
    """Validate that the request header contains a key named 'Authorization'
    and that its value matches the DS_SECRET_TOKEN environment variable.

    See https://github.com/tiangolo/fastapi/issues/142#issuecomment-688566673
    """
    if api_key_header != os.getenv('DS_SECRET_TOKEN'):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )
