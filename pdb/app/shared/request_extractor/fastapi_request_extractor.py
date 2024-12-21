from pdb.app.shared.request_extractor.request_extractor import RequestExtractor
from typing import Any

from fastapi import Request


class FastApiRequestExtractor(RequestExtractor):
    def __init__(self) -> None:
        pass

    def request_as_dict(self, request: Request) -> dict[str, Any]:
        data = {"url": request.url}
        data.update(request.cookies)
        data.update(request.headers)
        data.update(request.path_params)
        data.update(request.query_params)
        return data
