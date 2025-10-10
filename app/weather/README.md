# BACKGROUND

THIS API IS AIM FOR QUERYING WEATHER FORECAST IN 3 DAYS.

## Usage

1. start up this API service (check out [this](../README.md)).
2. send request to the API endpoint.

::: code-group
```base.sh
curl -X POST -H "Content-Type: application/json" -d '{"city": "青浦"}' http://localhost:8000/api/weather/forecast
```
```all.sh
curl -X POST -H "Content-Type: application/json" -d '{
    "city": "沈阳市铁西区",
    "extensions": "all"
}' http://localhost:8000/api/weather/forecast
```
:::
