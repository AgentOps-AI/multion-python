# This file was auto-generated by Fern from our API Definition.

import os
import typing
from json.decoder import JSONDecodeError

import httpx

from .core.api_error import ApiError
from .core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from .core.request_options import RequestOptions
from .core.unchecked_base_model import construct_type
from .environment import MultiOnEnvironment
from .errors.bad_request_error import BadRequestError
from .errors.internal_server_error import InternalServerError
from .errors.payment_required_error import PaymentRequiredError
from .errors.unauthorized_error import UnauthorizedError
from .errors.unprocessable_entity_error import UnprocessableEntityError
from .sessions.client import AsyncSessionsClient, SessionsClient
from .types.bad_request_response import BadRequestResponse
from .types.browse_output import BrowseOutput
from .types.http_validation_error import HttpValidationError
from .types.internal_server_error_response import InternalServerErrorResponse
from .types.mode import Mode
from .types.payment_required_response import PaymentRequiredResponse
from .types.retrieve_output import RetrieveOutput
from .types.unauthorized_response import UnauthorizedResponse

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class BaseMultiOn:
    """
    Use this class to access the different functions within the SDK. You can instantiate any number of clients with different configuration that will propagate to these functions.

    Parameters
    ----------
    base_url : typing.Optional[str]
        The base url to use for requests from the client.

    environment : MultiOnEnvironment
        The environment to use for requests from the client. from .environment import MultiOnEnvironment



        Defaults to MultiOnEnvironment.DEFAULT



    api_key : typing.Optional[str]
    timeout : typing.Optional[float]
        The timeout to be used, in seconds, for requests. By default the timeout is 180 seconds, unless a custom httpx client is used, in which case this default is not enforced.

    follow_redirects : typing.Optional[bool]
        Whether the default httpx client follows redirects or not, this is irrelevant if a custom httpx client is passed in.

    httpx_client : typing.Optional[httpx.Client]
        The httpx client to use for making requests, a preconfigured client is used by default, however this is useful should you want to pass in any custom httpx configuration.

    Examples
    --------
    from multion.client import MultiOn

    client = MultiOn(
        api_key="YOUR_API_KEY",
    )
    """

    def __init__(
        self,
        *,
        base_url: typing.Optional[str] = None,
        environment: MultiOnEnvironment = MultiOnEnvironment.DEFAULT,
        api_key: typing.Optional[str] = os.getenv("MULTION_API_KEY"),
        timeout: typing.Optional[float] = None,
        follow_redirects: typing.Optional[bool] = True,
        httpx_client: typing.Optional[httpx.Client] = None
    ):
        _defaulted_timeout = timeout if timeout is not None else 180 if httpx_client is None else None
        if api_key is None:
            raise ApiError(
                body="The client must be instantiated be either passing in api_key or setting MULTION_API_KEY"
            )
        self._client_wrapper = SyncClientWrapper(
            base_url=_get_base_url(base_url=base_url, environment=environment),
            api_key=api_key,
            httpx_client=httpx_client
            if httpx_client is not None
            else httpx.Client(timeout=_defaulted_timeout, follow_redirects=follow_redirects)
            if follow_redirects is not None
            else httpx.Client(timeout=_defaulted_timeout),
            timeout=_defaulted_timeout,
        )
        self.sessions = SessionsClient(client_wrapper=self._client_wrapper)

    def browse(
        self,
        *,
        cmd: str,
        url: typing.Optional[str] = OMIT,
        local: typing.Optional[bool] = OMIT,
        session_id: typing.Optional[str] = OMIT,
        max_steps: typing.Optional[int] = OMIT,
        include_screenshot: typing.Optional[bool] = OMIT,
        temperature: typing.Optional[float] = OMIT,
        mode: typing.Optional[Mode] = OMIT,
        use_proxy: typing.Optional[bool] = OMIT,
        request_options: typing.Optional[RequestOptions] = None
    ) -> BrowseOutput:
        """
        Allows for browsing the web using detailed natural language commands.

        The function supports multi-step command execution based on the `CONTINUE` status of the Agent.

        Parameters
        ----------
        cmd : str
            A specific natural language instruction for the agent to execute

        url : typing.Optional[str]
            The URL to start or continue browsing from. (Default: google.com)

        local : typing.Optional[bool]
            Boolean flag to indicate if session to be run locally or in the cloud (Default: False). If set to true, the session will be run locally via your chrome extension. If set to false, the session will be run in the cloud.

        session_id : typing.Optional[str]
            Continues the session with session_id if provided.

        max_steps : typing.Optional[int]
            Maximum number of steps to execute. (Default: 20)

        include_screenshot : typing.Optional[bool]
            Boolean flag to include a screenshot of the final page. (Default: False)

        temperature : typing.Optional[float]
            The temperature of model

        mode : typing.Optional[Mode]

        use_proxy : typing.Optional[bool]
            Boolean flag to use a proxy for the session (Default: False). Each Session gets a new Residential IP.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        BrowseOutput
            Successful Response

        Examples
        --------
        from multion.client import MultiOn

        client = MultiOn(
            api_key="YOUR_API_KEY",
        )
        client.browse(
            cmd="Find the top comment of the top post on Hackernews.",
            url="https://news.ycombinator.com/",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            "browse",
            method="POST",
            json={
                "cmd": cmd,
                "url": url,
                "local": local,
                "session_id": session_id,
                "max_steps": max_steps,
                "include_screenshot": include_screenshot,
                "temperature": temperature,
                "mode": mode,
                "use_proxy": use_proxy,
            },
            request_options=request_options,
            omit=OMIT,
        )
        if 200 <= _response.status_code < 300:
            return typing.cast(BrowseOutput, construct_type(type_=BrowseOutput, object_=_response.json()))  # type: ignore
        if _response.status_code == 400:
            raise BadRequestError(
                typing.cast(BadRequestResponse, construct_type(type_=BadRequestResponse, object_=_response.json()))  # type: ignore
            )
        if _response.status_code == 401:
            raise UnauthorizedError(
                typing.cast(UnauthorizedResponse, construct_type(type_=UnauthorizedResponse, object_=_response.json()))  # type: ignore
            )
        if _response.status_code == 402:
            raise PaymentRequiredError(
                typing.cast(PaymentRequiredResponse, construct_type(type_=PaymentRequiredResponse, object_=_response.json()))  # type: ignore
            )
        if _response.status_code == 422:
            raise UnprocessableEntityError(
                typing.cast(HttpValidationError, construct_type(type_=HttpValidationError, object_=_response.json()))  # type: ignore
            )
        if _response.status_code == 500:
            raise InternalServerError(
                typing.cast(InternalServerErrorResponse, construct_type(type_=InternalServerErrorResponse, object_=_response.json()))  # type: ignore
            )
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def retrieve(
        self,
        *,
        cmd: str,
        url: typing.Optional[str] = OMIT,
        session_id: typing.Optional[str] = OMIT,
        local: typing.Optional[bool] = OMIT,
        fields: typing.Optional[typing.Sequence[str]] = OMIT,
        format: typing.Optional[typing.Literal["json"]] = OMIT,
        max_items: typing.Optional[float] = OMIT,
        full_page: typing.Optional[bool] = OMIT,
        render_js: typing.Optional[bool] = OMIT,
        scroll_to_bottom: typing.Optional[bool] = OMIT,
        include_screenshot: typing.Optional[bool] = OMIT,
        request_options: typing.Optional[RequestOptions] = None
    ) -> RetrieveOutput:
        """
        Retrieve data from webpage based on a url and natural language command that guides agents data extraction process.

        The function can create a new session or be used as part of a session.

        Parameters
        ----------
        cmd : str
            A specific natural language instruction on data the agent should extract.

        url : typing.Optional[str]
            The URL to create or continue session from.

        session_id : typing.Optional[str]
            Continues the session with session_id if provided.

        local : typing.Optional[bool]
            Boolean flag to indicate if session to be run locally or in the cloud (Default: False). If set to true, the session will be run locally via your chrome extension. If set to false, the session will be run in the cloud.

        fields : typing.Optional[typing.Sequence[str]]
            List of fields (columns) to be outputted in data.

        format : typing.Optional[typing.Literal["json"]]
            Format of response data. (Default: json)

        max_items : typing.Optional[float]
            Maximum number of data items to retrieve. (Default: 100)

        full_page : typing.Optional[bool]
            Flag to retrieve full page (Default: True). If set to false, the data will only be retrieved from the current session viewport.

        render_js : typing.Optional[bool]
            Flag to include rich JS and ARIA elements in data retrieved. (Default: False)

        scroll_to_bottom : typing.Optional[bool]
            Flag to scroll to the bottom of the page (Default: False). If set to true, the page will be scrolled to the bottom for a maximum of 5 seconds before data is retrieved.

        include_screenshot : typing.Optional[bool]
            Flag to include a screenshot with the response. (Default: False)

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        RetrieveOutput
            Successful Response

        Examples
        --------
        from multion.client import MultiOn

        client = MultiOn(
            api_key="YOUR_API_KEY",
        )
        client.retrieve(
            cmd="Find the top comment of the top post on Hackernews and get its title and points.",
            url="https://news.ycombinator.com/",
            fields=["title", "points"],
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            "retrieve",
            method="POST",
            json={
                "cmd": cmd,
                "url": url,
                "session_id": session_id,
                "local": local,
                "fields": fields,
                "format": format,
                "max_items": max_items,
                "full_page": full_page,
                "render_js": render_js,
                "scroll_to_bottom": scroll_to_bottom,
                "include_screenshot": include_screenshot,
            },
            request_options=request_options,
            omit=OMIT,
        )
        if 200 <= _response.status_code < 300:
            return typing.cast(RetrieveOutput, construct_type(type_=RetrieveOutput, object_=_response.json()))  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(
                typing.cast(HttpValidationError, construct_type(type_=HttpValidationError, object_=_response.json()))  # type: ignore
            )
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncBaseMultiOn:
    """
    Use this class to access the different functions within the SDK. You can instantiate any number of clients with different configuration that will propagate to these functions.

    Parameters
    ----------
    base_url : typing.Optional[str]
        The base url to use for requests from the client.

    environment : MultiOnEnvironment
        The environment to use for requests from the client. from .environment import MultiOnEnvironment



        Defaults to MultiOnEnvironment.DEFAULT



    api_key : typing.Optional[str]
    timeout : typing.Optional[float]
        The timeout to be used, in seconds, for requests. By default the timeout is 180 seconds, unless a custom httpx client is used, in which case this default is not enforced.

    follow_redirects : typing.Optional[bool]
        Whether the default httpx client follows redirects or not, this is irrelevant if a custom httpx client is passed in.

    httpx_client : typing.Optional[httpx.AsyncClient]
        The httpx client to use for making requests, a preconfigured client is used by default, however this is useful should you want to pass in any custom httpx configuration.

    Examples
    --------
    from multion.client import AsyncMultiOn

    client = AsyncMultiOn(
        api_key="YOUR_API_KEY",
    )
    """

    def __init__(
        self,
        *,
        base_url: typing.Optional[str] = None,
        environment: MultiOnEnvironment = MultiOnEnvironment.DEFAULT,
        api_key: typing.Optional[str] = os.getenv("MULTION_API_KEY"),
        timeout: typing.Optional[float] = None,
        follow_redirects: typing.Optional[bool] = True,
        httpx_client: typing.Optional[httpx.AsyncClient] = None
    ):
        _defaulted_timeout = timeout if timeout is not None else 180 if httpx_client is None else None
        if api_key is None:
            raise ApiError(
                body="The client must be instantiated be either passing in api_key or setting MULTION_API_KEY"
            )
        self._client_wrapper = AsyncClientWrapper(
            base_url=_get_base_url(base_url=base_url, environment=environment),
            api_key=api_key,
            httpx_client=httpx_client
            if httpx_client is not None
            else httpx.AsyncClient(timeout=_defaulted_timeout, follow_redirects=follow_redirects)
            if follow_redirects is not None
            else httpx.AsyncClient(timeout=_defaulted_timeout),
            timeout=_defaulted_timeout,
        )
        self.sessions = AsyncSessionsClient(client_wrapper=self._client_wrapper)

    async def browse(
        self,
        *,
        cmd: str,
        url: typing.Optional[str] = OMIT,
        local: typing.Optional[bool] = OMIT,
        session_id: typing.Optional[str] = OMIT,
        max_steps: typing.Optional[int] = OMIT,
        include_screenshot: typing.Optional[bool] = OMIT,
        temperature: typing.Optional[float] = OMIT,
        mode: typing.Optional[Mode] = OMIT,
        use_proxy: typing.Optional[bool] = OMIT,
        request_options: typing.Optional[RequestOptions] = None
    ) -> BrowseOutput:
        """
        Allows for browsing the web using detailed natural language commands.

        The function supports multi-step command execution based on the `CONTINUE` status of the Agent.

        Parameters
        ----------
        cmd : str
            A specific natural language instruction for the agent to execute

        url : typing.Optional[str]
            The URL to start or continue browsing from. (Default: google.com)

        local : typing.Optional[bool]
            Boolean flag to indicate if session to be run locally or in the cloud (Default: False). If set to true, the session will be run locally via your chrome extension. If set to false, the session will be run in the cloud.

        session_id : typing.Optional[str]
            Continues the session with session_id if provided.

        max_steps : typing.Optional[int]
            Maximum number of steps to execute. (Default: 20)

        include_screenshot : typing.Optional[bool]
            Boolean flag to include a screenshot of the final page. (Default: False)

        temperature : typing.Optional[float]
            The temperature of model

        mode : typing.Optional[Mode]

        use_proxy : typing.Optional[bool]
            Boolean flag to use a proxy for the session (Default: False). Each Session gets a new Residential IP.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        BrowseOutput
            Successful Response

        Examples
        --------
        from multion.client import AsyncMultiOn

        client = AsyncMultiOn(
            api_key="YOUR_API_KEY",
        )
        await client.browse(
            cmd="Find the top comment of the top post on Hackernews.",
            url="https://news.ycombinator.com/",
        )
        """
        _response = await self._client_wrapper.httpx_client.request(
            "browse",
            method="POST",
            json={
                "cmd": cmd,
                "url": url,
                "local": local,
                "session_id": session_id,
                "max_steps": max_steps,
                "include_screenshot": include_screenshot,
                "temperature": temperature,
                "mode": mode,
                "use_proxy": use_proxy,
            },
            request_options=request_options,
            omit=OMIT,
        )
        if 200 <= _response.status_code < 300:
            return typing.cast(BrowseOutput, construct_type(type_=BrowseOutput, object_=_response.json()))  # type: ignore
        if _response.status_code == 400:
            raise BadRequestError(
                typing.cast(BadRequestResponse, construct_type(type_=BadRequestResponse, object_=_response.json()))  # type: ignore
            )
        if _response.status_code == 401:
            raise UnauthorizedError(
                typing.cast(UnauthorizedResponse, construct_type(type_=UnauthorizedResponse, object_=_response.json()))  # type: ignore
            )
        if _response.status_code == 402:
            raise PaymentRequiredError(
                typing.cast(PaymentRequiredResponse, construct_type(type_=PaymentRequiredResponse, object_=_response.json()))  # type: ignore
            )
        if _response.status_code == 422:
            raise UnprocessableEntityError(
                typing.cast(HttpValidationError, construct_type(type_=HttpValidationError, object_=_response.json()))  # type: ignore
            )
        if _response.status_code == 500:
            raise InternalServerError(
                typing.cast(InternalServerErrorResponse, construct_type(type_=InternalServerErrorResponse, object_=_response.json()))  # type: ignore
            )
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def retrieve(
        self,
        *,
        cmd: str,
        url: typing.Optional[str] = OMIT,
        session_id: typing.Optional[str] = OMIT,
        local: typing.Optional[bool] = OMIT,
        fields: typing.Optional[typing.Sequence[str]] = OMIT,
        format: typing.Optional[typing.Literal["json"]] = OMIT,
        max_items: typing.Optional[float] = OMIT,
        full_page: typing.Optional[bool] = OMIT,
        render_js: typing.Optional[bool] = OMIT,
        scroll_to_bottom: typing.Optional[bool] = OMIT,
        include_screenshot: typing.Optional[bool] = OMIT,
        request_options: typing.Optional[RequestOptions] = None
    ) -> RetrieveOutput:
        """
        Retrieve data from webpage based on a url and natural language command that guides agents data extraction process.

        The function can create a new session or be used as part of a session.

        Parameters
        ----------
        cmd : str
            A specific natural language instruction on data the agent should extract.

        url : typing.Optional[str]
            The URL to create or continue session from.

        session_id : typing.Optional[str]
            Continues the session with session_id if provided.

        local : typing.Optional[bool]
            Boolean flag to indicate if session to be run locally or in the cloud (Default: False). If set to true, the session will be run locally via your chrome extension. If set to false, the session will be run in the cloud.

        fields : typing.Optional[typing.Sequence[str]]
            List of fields (columns) to be outputted in data.

        format : typing.Optional[typing.Literal["json"]]
            Format of response data. (Default: json)

        max_items : typing.Optional[float]
            Maximum number of data items to retrieve. (Default: 100)

        full_page : typing.Optional[bool]
            Flag to retrieve full page (Default: True). If set to false, the data will only be retrieved from the current session viewport.

        render_js : typing.Optional[bool]
            Flag to include rich JS and ARIA elements in data retrieved. (Default: False)

        scroll_to_bottom : typing.Optional[bool]
            Flag to scroll to the bottom of the page (Default: False). If set to true, the page will be scrolled to the bottom for a maximum of 5 seconds before data is retrieved.

        include_screenshot : typing.Optional[bool]
            Flag to include a screenshot with the response. (Default: False)

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        RetrieveOutput
            Successful Response

        Examples
        --------
        from multion.client import AsyncMultiOn

        client = AsyncMultiOn(
            api_key="YOUR_API_KEY",
        )
        await client.retrieve(
            cmd="Find the top comment of the top post on Hackernews and get its title and points.",
            url="https://news.ycombinator.com/",
            fields=["title", "points"],
        )
        """
        _response = await self._client_wrapper.httpx_client.request(
            "retrieve",
            method="POST",
            json={
                "cmd": cmd,
                "url": url,
                "session_id": session_id,
                "local": local,
                "fields": fields,
                "format": format,
                "max_items": max_items,
                "full_page": full_page,
                "render_js": render_js,
                "scroll_to_bottom": scroll_to_bottom,
                "include_screenshot": include_screenshot,
            },
            request_options=request_options,
            omit=OMIT,
        )
        if 200 <= _response.status_code < 300:
            return typing.cast(RetrieveOutput, construct_type(type_=RetrieveOutput, object_=_response.json()))  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(
                typing.cast(HttpValidationError, construct_type(type_=HttpValidationError, object_=_response.json()))  # type: ignore
            )
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


def _get_base_url(*, base_url: typing.Optional[str] = None, environment: MultiOnEnvironment) -> str:
    if base_url is not None:
        return base_url
    elif environment is not None:
        return environment.value
    else:
        raise Exception("Please pass in either base_url or environment to construct the client")
