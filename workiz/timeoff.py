"""Time Off resource for Workiz API."""

from typing import Dict, Any, List
from .client import WorkizClient


class TimeOff:
    """Time Off resource handler for Workiz API.

    The Time Off resource allows you to fetch time off information for users.
    """

    def __init__(self, client: WorkizClient):
        self.client = client

    def get_all(self, all: bool = False) -> List[Dict[str, Any]]:
        """Get time off details for all users or company-wide.

        Args:
            all: If True, get all users and company time off (default: False)

        Returns:
            List of time off dictionaries containing:
            - start: Start datetime string
            - end: End datetime string
            - userName: Name of the user or "Entire Business"

        Example:
            >>> time_offs = client.timeoff.get_all(all=True)
        """
        endpoint = "TimeOff/get/"
        params = {"all": all}
        return self.client.get(endpoint, params=params)

    def get(self, user_name: str) -> List[Dict[str, Any]]:
        """Get time off details for a specific user.

        Args:
            user_name: The user's name

        Returns:
            List of time off dictionaries containing:
            - start: Start datetime string
            - end: End datetime string
            - userName: Name of the user

        Example:
            >>> user_time_offs = client.timeoff.get("Joe Acme")
        """
        endpoint = f"TimeOff/get/{user_name}"
        return self.client.get(endpoint)