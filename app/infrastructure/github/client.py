from typing import Optional

from aiohttp import ClientSession, ClientTimeout

from .schemas import Repository


class GitHub:
    BASE_URL = "https://api.github.com"

    def __init__(self):
        self._session: Optional[ClientSession] = None

    @property
    def session(self) -> ClientSession:
        """
        Get session
        """
        if self._session is None or self._session.closed:
            self._session = ClientSession(
                timeout=ClientTimeout(total=15),
            )
        return self._session

    async def close(self) -> None:
        """
        Close session
        """
        if self._session is not None and not self._session.closed:
            await self._session.close()

    async def search_repositories(
        self,
        text: str,
        **kwargs: str,
    ) -> list[Repository]:
        """
        Search repositories by a raw query

        :text: The raw query
        :kwargs: The query parameters

        :examples:
        >>> search_repositories("text", sort="stars", order="desc")
        >>> search_repositories("text")
        >>> search_repositories("", language="Python")
        """
        params = {}
        if sort_type := kwargs.pop("sort", None):
            params["sort"] = sort_type
        if order_type := kwargs.pop("order", None):
            params["order"] = order_type
        params["q"] = "{text} {keywords}".format(
            text=text,
            keywords=" ".join(
                f"{keyword}:{value}"
                for keyword, value in kwargs.items()
            ),
        ).strip()

        result = await self.session.get(
            f"{self.BASE_URL}/search/repositories",
            params=params,
        )
        result.raise_for_status()

        response = await result.json()

        return [
            Repository(**item)
            for item in response["items"]
        ]
