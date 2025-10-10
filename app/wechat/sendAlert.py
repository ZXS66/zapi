from dataclasses import dataclass
from datetime import datetime, timedelta
from fastapi import APIRouter
from pydantic import BaseModel
import requests

from app.constants import (
    WECHAT_APPID,
    WECHAT_APPSECRET,
    WECHAT_TEMPLATEID,
    WECHAT_TOUSERS,
)

router = APIRouter()


class AlertForm(BaseModel):
    appName: str
    errName: str
    callstack: str | None = None


@dataclass
class AccessTokenWithExpiration:
    access_token: str
    """access token for sending messages"""
    expires_in: int
    """expiry time in seconds"""
    obtained_at: datetime


def __getAccessToken():
    resp = requests.get(
        f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={WECHAT_APPID}&secret={WECHAT_APPSECRET}"
    ).json()
    return AccessTokenWithExpiration(
        resp["access_token"], resp["expires_in"], datetime.now()
    )


async def __sendAlert(access_token: str, touser: str, template_id: str, af: AlertForm):
    data = {
        "touser": touser,
        "template_id": template_id,
        "url": "https://weixin.qq.com/download",
        "data": {
            "appName": {"value": af.appName},
            "errName": {"value": af.errName},
            "callstack": {"value": af.callstack or ""},
        },
    }
    return requests.post(
        f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={access_token}",
        json=data,
    )


__access_token = __getAccessToken()


@router.post("/sendAlert")
async def send(af: AlertForm):
    global __access_token
    if (
        __access_token.obtained_at + timedelta(seconds=__access_token.expires_in - 8)
    ) < datetime.now():
        # less than 8 seconds before expiration
        __access_token = __getAccessToken()
    for user in WECHAT_TOUSERS:
        await __sendAlert(__access_token.access_token, user, WECHAT_TEMPLATEID, af)
    return "ok"
