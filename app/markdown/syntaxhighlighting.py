from fastapi import APIRouter, Depends, HTTPException
from markdown_it import MarkdownIt
from pydantic import BaseModel
from requests import get as fetch

from app.dependencies import get_token_header
from app.utils import isNoneOrEmptyStr

router = APIRouter()


class SyntaxHighlightingForm(BaseModel):
    """请求参数"""

    lang: str
    """programming language"""
    url: str | None = None
    """URL of hosted source code（e.g.: github.com）"""
    source: str | None = None
    """source code (alternative)"""


@router.post(
    "/syntaxhighlighting", dependencies=[Depends(get_token_header)], deprecated=True
)
async def syntaxhighlighting(form: SyntaxHighlightingForm):
    if len(form.lang) == 0 or (
        isNoneOrEmptyStr(form.url) and isNoneOrEmptyStr(form.source)
    ):
        raise HTTPException(status_code=400, detail="invalid form data")

    sourcecode: str = form.source or ""
    if form.url is not None and not isNoneOrEmptyStr(form.url):
        # by url
        try:
            resp = fetch(form.url, timeout=(32, 64))
            sourcecode = f"```{form.lang}\n{resp.text}\n```"
        except Exception as e:
            sourcecode = (
                f"```error ({e}) occurred when fetching response from {form.url}```"
            )

    md = MarkdownIt("commonmark", {"breaks": True, "html": True})
    return md.render(sourcecode)
