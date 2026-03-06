"""Base client for Workiz API."""

import requests
from typing import Optional, Dict, Any
from .exceptions import WorkizAPIError, WorkizAuthenticationError
from .jobs import Jobs
from .leads import Leads
from .team import Team
from .timeoff import TimeOff


class WorkizClient:
    """Main client for interacting with the Workiz API.

    Args:
        api_token: Your Workiz API token (used in URL path)
        auth_secret: Your Workiz auth secret (used in request bodies)
        base_url: Base URL for the API (default: https://api.workiz.com/api/v1)

    Example:
        >>> from workiz import WorkizClient
        >>> client = WorkizClient(api_token="your_token", auth_secret="your_secret")
        >>> jobs = client.jobs.all()
        >>> lead = client.leads.get("uuid-here")
    """

    def __init__(
        self,
        api_token: str,
        auth_secret: str,
        base_url: str = "https://api.workiz.com/api/v1",
    ):
        self.api_token = api_token
        self.auth_secret = auth_secret
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

        # Initialize resource handlers
        self.jobs = Jobs(self)
        self.leads = Leads(self)
        self.team = Team(self)
        self.timeoff = TimeOff(self)

    def _get_url(self, endpoint: str) -> str:
        """Construct the full URL for an API endpoint.

        Args:
            endpoint: API endpoint path (e.g., '/job/get/123/')

        Returns:
            Full URL including base URL and API token
        """
        endpoint = endpoint.lstrip("/")
        return f"{self.base_url}/{self.api_token}/{endpoint}"

    def _handle_response(self, response: requests.Response) -> Any:
        """Handle API response and raise appropriate exceptions.

        Args:
            response: Response object from requests library

        Returns:
            JSON data from response

        Raises:
            WorkizAuthenticationError: If authentication fails
            WorkizAPIError: If API returns an error
        """
        try:
            data = response.json()
        except ValueError:
            # If response is not JSON, raise with status code
            response.raise_for_status()
            return None

        # Check for error responses
        if isinstance(data, dict) and data.get("error"):
            error_msg = data.get("msg", "Unknown error")
            error_code = data.get("code")
            error_details = data.get("details", [])

            if error_code == 401:
                raise WorkizAuthenticationError(error_msg)
            else:
                raise WorkizAPIError(error_msg, code=error_code, details=error_details)

        # Raise for HTTP errors that weren't caught above
        response.raise_for_status()

        return data

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Make an HTTP request to the API.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            params: Query parameters
            json_data: JSON body data (will include auth_secret automatically)

        Returns:
            Response data from API
        """
        url = self._get_url(endpoint)

        # Add auth_secret to JSON body for POST requests
        if json_data is not None and isinstance(json_data, dict):
            json_data = json_data.copy()
            json_data["auth_secret"] = self.auth_secret

        response = self.session.request(
            method=method,
            url=url,
            params=params,
            json=json_data,
            headers={"Accept": "application/json", "Content-Type": "application/json"},
        )

        return self._handle_response(response)

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """Make a GET request to the API.

        Args:
            endpoint: API endpoint path
            params: Query parameters

        Returns:
            Response data from API
        """
        return self._request("GET", endpoint, params=params)

    def post(
        self,
        endpoint: str,
        json_data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Make a POST request to the API.

        Args:
            endpoint: API endpoint path
            json_data: JSON body data
            params: Query parameters

        Returns:
            Response data from API
        """
        return self._request("POST", endpoint, json_data=json_data, params=params)