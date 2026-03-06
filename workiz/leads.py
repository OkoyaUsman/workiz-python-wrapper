"""Leads resource for Workiz API."""

from typing import Optional, Dict, Any, List
from .client import WorkizClient


class Leads:
    """Leads resource handler for Workiz API.

    The Lead resource is the primary object of Workiz.
    You can create, update, assign users, change a status and update custom fields.
    """

    def __init__(self, client: WorkizClient):
        self.client = client

    def get(self, uuid: str) -> Dict[str, Any]:
        """Get lead details by UUID.

        Args:
            uuid: The lead's unique UUID

        Returns:
            Lead details dictionary

        Example:
            >>> lead = client.leads.get("3fa85f64-5717-4562-b3fc-2c963f66afa6")
        """
        endpoint = f"lead/get/{uuid}/"
        return self.client.get(endpoint)

    def all(
        self,
        start_date: Optional[str] = None,
        offset: int = 0,
        records: int = 100,
        only_open: bool = True,
        status: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """Get a list of leads.

        The lead list is sorted by the LeadDateTime field and by default is ordered
        descending, most recently scheduled lead.

        Args:
            start_date: Date range starting from this date until today (yyyy-MM-dd).
                        If not provided, defaults to last 14 days.
            offset: Record offset (default: 0)
            records: Number of records to retrieve, maximum 100 (default: 100)
            only_open: Only list open leads, excluding Done and Canceled statuses (default: True)
            status: Array of lead statuses to filter by

        Returns:
            List of lead dictionaries

        Example:
            >>> leads = client.leads.all(start_date="2024-01-01", records=50)
        """
        params: Dict[str, Any] = {
            "offset": offset,
            "records": records,
            "only_open": only_open,
        }

        if start_date:
            params["start_date"] = start_date
        if status:
            params["status"] = status

        endpoint = "lead/all/"
        return self.client.get(endpoint, params=params)

    def create(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new lead.

        Args:
            lead_data: Dictionary containing lead information. Required fields include:
                      - LeadDateTime: ISO datetime string
                      - ClientId: Client ID
                      - Phone: Phone number
                      - Email: Email address
                      - FirstName: First name
                      - LastName: Last name
                      - Company: Company name
                      - Address: Street address
                      - City: City
                      - State: State code
                      - PostalCode: Postal/ZIP code
                      - Country: Country code
                      Optional fields:
                      - LeadEndDateTime: ISO datetime string
                      - LeadLost: Lead lost flag (0 or 1)
                      - PhoneExt: Phone extension
                      - SecondPhone: Second phone number
                      - SecondPhoneExt: Second phone extension
                      - Unit: Unit number
                      - JobType: Type of job
                      - ReferralCompany: Referral company name
                      - Timezone: Timezone (e.g., "US/Pacific")
                      - JobSource: Source of the lead
                      - LeadNotes: Notes about the lead
                      - CreatedBy: Creator name
                      - Created: ISO datetime string
                      - ServiceArea: Service area identifier

        Returns:
            Response dictionary with flag, data containing UUID, ClientId, and link

        Example:
            >>> lead_data = {
            ...     "LeadDateTime": "2024-01-15T09:00:00Z",
            ...     "ClientId": 1002,
            ...     "Phone": "6195555555",
            ...     "Email": "client@example.com",
            ...     "FirstName": "Joe",
            ...     "LastName": "Acme",
            ...     "Company": "Acme Inc",
            ...     "Address": "123 W Main Street",
            ...     "City": "San Diego",
            ...     "State": "CA",
            ...     "PostalCode": "92109",
            ...     "Country": "US"
            ... }
            >>> result = client.leads.create(lead_data)
        """
        endpoint = "lead/create/"
        return self.client.post(endpoint, json_data=lead_data)

    def update(self, uuid: str, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a lead's information.

        Args:
            uuid: The lead's unique UUID (required)
            lead_data: Dictionary containing fields to update. Can include any lead fields
                      such as Status, LeadDateTime, LeadEndDateTime, ClientId, Company,
                      Phone, Email, Address fields, JobType, LeadNotes, Tags, etc.

        Returns:
            Response dictionary with flag, data containing UUID, ClientId, and link

        Example:
            >>> update_data = {
            ...     "Status": "In progress",
            ...     "LeadNotes": "Updated notes"
            ... }
            >>> result = client.leads.update("XYZ56X", update_data)
        """
        lead_data = lead_data.copy()
        lead_data["UUID"] = uuid
        endpoint = "lead/update/"
        return self.client.post(endpoint, json_data=lead_data)

    def assign(self, uuid: str, user: str) -> Dict[str, Any]:
        """Assign a user to a lead.

        Args:
            uuid: The lead's unique UUID
            user: Name of the user to assign

        Returns:
            Response dictionary with flag, data containing UUID, LeadId, and link

        Example:
            >>> result = client.leads.assign("XYZ56X", "Alex Wilson")
        """
        endpoint = "lead/assign/"
        json_data = {"UUID": uuid, "User": user}
        return self.client.post(endpoint, json_data=json_data)

    def unassign(self, uuid: str, user: str) -> Dict[str, Any]:
        """Unassign a user from a lead.

        Args:
            uuid: The lead's unique UUID
            user: Name of the user to unassign

        Returns:
            Response dictionary with flag, data containing UUID, LeadId, and link

        Example:
            >>> result = client.leads.unassign("XYZ56X", "Alex Wilson")
        """
        endpoint = "lead/unassign/"
        json_data = {"UUID": uuid, "User": user}
        return self.client.post(endpoint, json_data=json_data)

    def mark_lost(self, uuid: str) -> Dict[str, Any]:
        """Mark a lead as lost.

        Args:
            uuid: The lead's unique UUID

        Returns:
            Response dictionary with flag, msg, and code

        Example:
            >>> result = client.leads.mark_lost("XYZ56X")
        """
        endpoint = f"lead/markLost/{uuid}/"
        return self.client.post(endpoint, json_data={})

    def activate(self, uuid: str) -> Dict[str, Any]:
        """Change a lost lead back to active.

        Args:
            uuid: The lead's unique UUID

        Returns:
            Response dictionary with flag, msg, and code

        Example:
            >>> result = client.leads.activate("XYZ56X")
        """
        endpoint = f"lead/activate/{uuid}/"
        return self.client.post(endpoint, json_data={})

    def convert(self, uuid: str) -> Dict[str, Any]:
        """Convert a lead to a job.

        Args:
            uuid: The lead's unique UUID

        Returns:
            Response dictionary with flag, data containing UUID, ClientId, and link

        Example:
            >>> result = client.leads.convert("XYZ56X")
        """
        endpoint = "lead/convert/"
        json_data = {"UUID": uuid}
        return self.client.post(endpoint, json_data=json_data)