# BACKGROUND

THIS API IS AIM FOR SENDING ALERT MESSAGES TO WECHAT USERS (ADDED USERS IN CONSOLE FIRST) VIA TEMPLATE MESSAGE。

## Usage

1. register a test account in [weixin console](https://mp.weixin.qq.com/debug/cgi-bin/sandboxinfo?action=showinfo&t=sandbox/index)
2. create a template message. caution: due to tencent's restrictions [^1][^2], the template message can't start or tail with variable render content. here is a sample:
```txt
Dear, your application {{appName.DATA}} got error of {{errName.DATA}}, please fix it ASAP.
Here is the call-stack: {{callstack.DATA}}.
```
3. scan the QR code to add user to the recipient list
4. copy `appID`, `appSecret`, `templateID`, `openID` to `.env` file (under the root folder of this repo)
5. run the `fastapi` service (see [README](../README.md)) and send POST request to `/wechat/sendAlert`. here is a sample:
```sh
curl -X POST -H "Content-Type: application/json" -d '{
    "appName": "MyApp",
    "errName": "TypeError",
    "callstack": "TypeError: unsupported operand type(s) for +: 'int' and 'str'"
}' http://localhost:8000/api/wechat/sendAlert
```

[^1]: [关于规范公众号模板消息的公告](https://mp.weixin.qq.com/s/xFhCqMnlQhwWJ64ueWN8hQ)
[^2]: [关于规范公众号模板消息的再次公告](https://mp.weixin.qq.com/cgi-bin/announce?action=getannouncement&announce_id=11680142498cInTZ&version=&lang=zh_CN&token=)
