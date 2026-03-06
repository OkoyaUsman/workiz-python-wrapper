"""Jobs resource for Workiz API."""

from typing import Optional, Dict, Any, List
from .client import WorkizClient


class Jobs:
    """Jobs resource handler for Workiz API.

    The Job resource is the primary object of Workiz.
    You can create, update, assign users, change a status and update custom fields.
    """

    def __init__(self, client: WorkizClient):
        self.client = client

    def get(self, uuid: str) -> Dict[str, Any]:
        """Get job details by UUID.

        Args:
            uuid: The job's unique UUID

        Returns:
            Job details dictionary

        Example:
            >>> job = client.jobs.get("XYZ55Y")
        """
        endpoint = f"job/get/{uuid}/"
        return self.client.get(endpoint)

    def all(
        self,
        start_date: Optional[str] = None,
        offset: int = 0,
        records: int = 100,
        only_open: bool = True,
        status: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """Get a list of jobs.

        The job list is sorted by the JobDateTime field and by default is ordered
        descending, most recently scheduled jobs.

        Args:
            start_date: Date range starting from this date until today (yyyy-MM-dd).
                        If not provided, defaults to last 14 days.
            offset: Record offset (default: 0)
            records: Number of records to retrieve, maximum 100 (default: 100)
            only_open: Only list open jobs, excluding Done and Canceled statuses (default: True)
            status: Array of job statuses to filter by

        Returns:
            List of job dictionaries

        Example:
            >>> jobs = client.jobs.all(start_date="2024-01-01", records=50)
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

        endpoint = "job/all/"
        return self.client.get(endpoint, params=params)

    def create(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new job.

        Args:
            job_data: Dictionary containing job information. Required fields include:
                     - JobDateTime: ISO datetime string
                     - ClientId: Client ID
                     - Company: Company name
                     - Phone: Phone number
                     - Email: Email address
                     - FirstName: First name
                     - LastName: Last name
                     - Address: Street address
                     - City: City
                     - State: State code
                     - Country: Country code
                     - PostalCode: Postal/ZIP code
                     Optional fields:
                     - JobEndDateTime: ISO datetime string
                     - PhoneExt: Phone extension
                     - SecondPhone: Second phone number
                     - SecondPhoneExt: Second phone extension
                     - Unit: Unit number
                     - JobType: Type of job
                     - ReferralCompany: Referral company name
                     - Timezone: Timezone (e.g., "US/Pacific")
                     - JobSource: Source of the job
                     - JobNotes: Notes about the job
                     - CreatedBy: Creator name
                     - Created: ISO datetime string
                     - ServiceArea: Service area identifier

        Returns:
            Response dictionary with flag, data containing UUID, ClientId, and link

        Example:
            >>> job_data = {
            ...     "JobDateTime": "2024-01-15T09:00:00Z",
            ...     "ClientId": 1002,
            ...     "Company": "Sample Company",
            ...     "Phone": "6195555555",
            ...     "Email": "client@example.com",
            ...     "FirstName": "Joe",
            ...     "LastName": "Acme",
            ...     "Address": "123 W Main Street",
            ...     "City": "San Diego",
            ...     "State": "CA",
            ...     "Country": "US",
            ...     "PostalCode": "92109"
            ... }
            >>> result = client.jobs.create(job_data)
        """
        endpoint = "job/create/"
        return self.client.post(endpoint, json_data=job_data)

    def update(self, uuid: str, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a job's information.

        Args:
            uuid: The job's unique UUID (required)
            job_data: Dictionary containing fields to update. Can include any job fields
                     such as Status, SubStatus, JobDateTime, JobEndDateTime, ClientId,
                     Company, Phone, Email, Address fields, JobType, JobNotes, Tags, etc.

        Returns:
            Response dictionary with flag, data containing UUID, ClientId, and link

        Example:
            >>> update_data = {
            ...     "Status": "In progress",
            ...     "JobNotes": "Updated notes"
            ... }
            >>> result = client.jobs.update("XYZ56X", update_data)
        """
        job_data = job_data.copy()
        job_data["UUID"] = uuid
        endpoint = "job/update/"
        return self.client.post(endpoint, json_data=job_data)

    def assign(self, uuid: str, user: str) -> Dict[str, Any]:
        """Assign a user to a job.

        Args:
            uuid: The job's unique UUID
            user: Name of the user to assign

        Returns:
            Response dictionary with flag, data containing UUID, ClientId, and link

        Example:
            >>> result = client.jobs.assign("XYZ56X", "Alex Wilson")
        """
        endpoint = "job/assign/"
        json_data = {"UUID": uuid, "User": user}
        return self.client.post(endpoint, json_data=json_data)

    def unassign(self, uuid: str, user: str) -> Dict[str, Any]:
        """Unassign a user from a job.

        Args:
            uuid: The job's unique UUID
            user: Name of the user to unassign

        Returns:
            Response dictionary with flag, data containing UUID, ClientId, and link

        Example:
            >>> result = client.jobs.unassign("XYZ56X", "Alex Wilson")
        """
        endpoint = "job/unassign/"
        json_data = {"UUID": uuid, "User": user}
        return self.client.post(endpoint, json_data=json_data)

    def add_payment(
        self,
        uuid: str,
        amount: float,
        payment_type: str,
        date: Optional[str] = None,
        reference: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Add a payment to a job.

        Args:
            uuid: The job's unique UUID
            amount: Payment amount
            payment_type: Type of payment - must be one of: "cash", "credit", "check"
            date: ISO datetime string for payment date (defaults to current time if not provided)
            reference: Payment reference number

        Returns:
            Response dictionary with flag, msg, and data containing paymentId

        Example:
            >>> result = client.jobs.add_payment(
            ...     "XYZ56X",
            ...     amount=100.00,
            ...     payment_type="cash",
            ...     date="2024-01-15T10:00:00Z",
            ...     reference="102235620"
            ... )
        """
        if payment_type not in ["cash", "credit", "check"]:
            raise ValueError(
                f"payment_type must be one of: 'cash', 'credit', 'check'. Got: {payment_type}"
            )

        endpoint = f"job/addPayment/{uuid}/"
        json_data: Dict[str, Any] = {
            "amount": amount,
            "type": payment_type,
        }

        if date:
            json_data["date"] = date
        if reference:
            json_data["reference"] = reference

        params = {"type": payment_type}
        return self.client.post(endpoint, json_data=json_data, params=params)