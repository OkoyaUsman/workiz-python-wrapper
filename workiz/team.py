"""Team resource for Workiz API."""

from typing import Dict, Any, List
from .client import WorkizClient


class Team:
    """Team resource handler for Workiz API.

    The Team resource represents users/team members in Workiz.
    Team members can be viewed individually or as a list.
    """

    def __init__(self, client: WorkizClient):
        self.client = client

    def all(self) -> List[Dict[str, Any]]:
        """Get a list of all active team members.

        Returns:
            List of team member dictionaries containing:
            - id: User ID
            - name: User name
            - created: Creation date (ISO datetime)
            - role: User role
            - fieldTech: Whether user is a field tech
            - email: User email
            - serviceAreas: List of service areas
            - skills: List of skills
            - active: Whether user is active

        Example:
            >>> team_members = client.team.all()
        """
        endpoint = "team/all/"
        return self.client.get(endpoint)

    def get(self, user_id: str) -> Dict[str, Any]:
        """Get specific user details by user ID.

        Args:
            user_id: The user's unique ID

        Returns:
            User details dictionary containing:
            - id: User ID
            - name: User name
            - created: Creation date (ISO datetime)
            - role: User role
            - fieldTech: Whether user is a field tech
            - email: User email
            - serviceAreas: List of service areas
            - skills: List of skills
            - active: Whether user is active

        Example:
            >>> user = client.team.get("34637")
        """
        endpoint = f"team/get/{user_id}"
        return self.client.get(endpoint)