from dataclasses import dataclass
# from dataclasses_json import dataclass_json
from typing import List, Literal, Optional
from requests import get as fetch
from json import load as jsonLoad, dumps as jsonDumps
from re import fullmatch
from asyncio import sleep as asleep
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    WebSocket,
    WebSocketDisconnect,
    WebSocketException,
    status
)
from pydantic import BaseModel

from app.dependencies import get_token_header, get_token_query
from app.wscm import WebSocketConnectionManager
from app.constants import AMAP_APP_KEY, IS_PROD_MODE, ZAPI_TOKEN

router = APIRouter()

class ForecastForm(BaseModel):
    """请求参数"""
    city: str
    """城市编码adcode"""
    extensions: Optional[Literal["base","all"]] = None
    """气象类型,base:返回实况天气,all:返回预报天气"""
    # key: Optional[str] = AMAP_API_KEY
    # """请求服务权限标识"""
    # output: Literal["JSON","XML"] = "JSON"
    # """返回格式"""

# @dataclass_json
@dataclass(frozen=True)
class AmapCity:
    city:str
    adcode:str
    citycode:Optional[str]

__cities:List[AmapCity] = []
with open("app/weather/cities.json",'r') as file:
    # __cities = AmapCity.from_dict(__cities)
    __temp = jsonLoad(file)
    for item in __temp:
        __cities.append(AmapCity(**item))


@router.get("/cities", dependencies=[Depends(get_token_header)])
async def cities():
    return __cities


def __getAmapCityByName(name:str) -> AmapCity:
    if fullmatch(r'\d+', name):
        # `name` is adcode, no conversion needed
        return AmapCity(name,name,name)

    if fullmatch(r'.+市.+[区县]?', name):
        # search by **市**区/县'
        city, district = name[:name.index('市')+1], name[name.index('市')+1:]
        flag = 0
        for ct in __cities:
            if not flag:
                # search by city first
                if ct.city == city:
                    flag = 1
            else:
                # then search by district
                if ct.city == district:
                    return ct

    # default search algorithm
    for ct in __cities:
        if ct.city and ct.city.startswith(name):
            return ct

    raise HTTPException(status_code=404, detail=f"the city ({name}) is not found")


@router.post("/forecast", dependencies=[Depends(get_token_header)])
async def forecast(form: ForecastForm):
    # city:str, extensions: Optional[Literal["base", "all"]]
    if len(form.city) == 0:
        raise HTTPException(status_code=400, detail="invalid form data")

    # https://lbs.amap.com/api/webservice/guide/api/weatherinfo
    theCity = __getAmapCityByName(form.city)
    AMAP_API_ENDPOINT = 'https://restapi.amap.com/v3/weather/weatherInfo'
    resp = fetch(
        AMAP_API_ENDPOINT,
        params={
            "key":AMAP_APP_KEY,
            "city": theCity.adcode,
            "extensions": form.extensions,
            "output": "JSON"
        }
    )
    return resp.json()

wscm = WebSocketConnectionManager()

@router.websocket("/forecast_ws/{client_id}", dependencies=[Depends(get_token_query)])
async def forecast_ws(websocket: WebSocket, client_id: Optional[str]=None):
    print(f"{client_id} is connected")
    try:
        await wscm.connect(websocket)
        data = await websocket.receive_json()
        while True:
            resp = await forecast(ForecastForm(**data))
            await wscm.send_personal_message(jsonDumps(resp), websocket)
            await asleep(16384 if IS_PROD_MODE else 16)
    except WebSocketDisconnect:
        print(f"{client_id} is disconnected")
        wscm.disconnect(websocket)
    except Exception as e:
        print(f"error occurred for {client_id}: {e}")
