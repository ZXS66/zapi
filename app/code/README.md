# BACKGROUND

THIS API IS USED FOR SYNTAX HIGHLIGHTING FOR SOURCE CODE.

## Usage

1. start up this API service (check out [this](../README.md)).
2. send request to the API endpoint.

```sh
curl -X POST -H "Content-Type: application/json" -d '{"lang":"yaml","url":"https://gitlab.com/ineo6/hosts/-/raw/master/next-hosts","source":null}' http://localhost:8000/api/code/syntaxhighlighting
```
