# Workiz Python Wrapper

A Python wrapper for the Workiz RESTful API that provides a simple and intuitive interface to interact with Workiz's job management, leads, team, and time off features.

## Installation

Install from PyPI:
```bash
pip install workiz
```

## Quick Start

```python
from workiz import WorkizClient

# Initialize the client
client = WorkizClient(
    api_token="your_api_token",
    auth_secret="your_auth_secret"
)

# Get all jobs
jobs = client.jobs.all(start_date="2024-01-01", records=50)

# Get a specific job
job = client.jobs.get("job-uuid-here")

# Create a new job
job_data = {
    "JobDateTime": "2024-01-15T09:00:00Z",
    "ClientId": 1002,
    "Company": "Sample Company",
    "Phone": "6195555555",
    "Email": "client@example.com",
    "FirstName": "Joe",
    "LastName": "Acme",
    "Address": "123 W Main Street",
    "City": "San Diego",
    "State": "CA",
    "Country": "US",
    "PostalCode": "92109"
}
result = client.jobs.create(job_data)

# Update a job
update_data = {
    "Status": "In progress",
    "JobNotes": "Updated notes"
}
client.jobs.update("job-uuid-here", update_data)

# Assign a user to a job
client.jobs.assign("job-uuid-here", "Alex Wilson")

# Add a payment to a job
client.jobs.add_payment(
    "job-uuid-here",
    amount=100.00,
    payment_type="cash",
    reference="102235620"
)
```

## Features

### Jobs
- `get(uuid)` - Get job details by UUID
- `all(start_date, offset, records, only_open, status)` - Get a list of jobs
- `create(job_data)` - Create a new job
- `update(uuid, job_data)` - Update a job's information
- `assign(uuid, user)` - Assign a user to a job
- `unassign(uuid, user)` - Unassign a user from a job
- `add_payment(uuid, amount, payment_type, date, reference)` - Add a payment to a job

### Leads
- `get(uuid)` - Get lead details by UUID
- `all(start_date, offset, records, only_open, status)` - Get a list of leads
- `create(lead_data)` - Create a new lead
- `update(uuid, lead_data)` - Update a lead's information
- `assign(uuid, user)` - Assign a user to a lead
- `unassign(uuid, user)` - Unassign a user from a lead
- `mark_lost(uuid)` - Mark a lead as lost
- `activate(uuid)` - Change a lost lead back to active
- `convert(uuid)` - Convert a lead to a job

### Team
- `all()` - Get a list of all active team members
- `get(user_id)` - Get specific user details by user ID

### Time Off
- `get_all(all)` - Get time off details for all users or company-wide
- `get(user_name)` - Get time off details for a specific user

## Examples

### Working with Jobs

```python
from workiz import WorkizClient

client = WorkizClient(api_token="your_token", auth_secret="your_secret")

# Get open jobs from the last 30 days
jobs = client.jobs.all(
    start_date="2024-01-01",
    only_open=True,
    records=100
)

# Filter jobs by status
jobs = client.jobs.all(
    start_date="2024-01-01",
    status=["Scheduled", "In progress"]
)

# Create a job with all fields
job_data = {
    "JobDateTime": "2024-01-15T09:00:00Z",
    "JobEndDateTime": "2024-01-15T17:00:00Z",
    "ClientId": 1002,
    "Company": "Acme Corporation",
    "Phone": "6195555555",
    "PhoneExt": "123",
    "Email": "contact@acme.com",
    "FirstName": "John",
    "LastName": "Doe",
    "Address": "123 Main St",
    "City": "San Diego",
    "State": "CA",
    "Country": "US",
    "PostalCode": "92109",
    "Unit": "Suite 100",
    "JobType": "Repair",
    "Timezone": "US/Pacific",
    "JobSource": "Website",
    "JobNotes": "Customer requested morning appointment",
    "ServiceArea": "metro1"
}
result = client.jobs.create(job_data)
```

### Working with Leads

```python
# Get all leads
leads = client.leads.all(start_date="2024-01-01")

# Create a lead
lead_data = {
    "LeadDateTime": "2024-01-15T09:00:00Z",
    "ClientId": 1002,
    "Phone": "6195555555",
    "Email": "lead@example.com",
    "FirstName": "Jane",
    "LastName": "Smith",
    "Company": "Smith Inc",
    "Address": "456 Oak Ave",
    "City": "Los Angeles",
    "State": "CA",
    "PostalCode": "90001",
    "Country": "US",
    "JobType": "Installation"
}
result = client.leads.create(lead_data)

# Convert a lead to a job
client.leads.convert("lead-uuid-here")

# Mark a lead as lost
client.leads.mark_lost("lead-uuid-here")

# Reactivate a lost lead
client.leads.activate("lead-uuid-here")
```

### Working with Team

```python
# Get all team members
team_members = client.team.all()

# Get a specific team member
user = client.team.get("34637")
print(f"User: {user['name']}, Email: {user['email']}")
```

### Working with Time Off

```python
# Get all time off entries
time_offs = client.timeoff.get_all(all=True)

# Get time off for a specific user
user_time_offs = client.timeoff.get("Joe Acme")
```

## Error Handling

The wrapper includes custom exceptions for better error handling:

```python
from workiz import WorkizClient, WorkizAPIError, WorkizAuthenticationError

try:
    client = WorkizClient(api_token="invalid", auth_secret="invalid")
    jobs = client.jobs.all()
except WorkizAuthenticationError as e:
    print(f"Authentication failed: {e}")
except WorkizAPIError as e:
    print(f"API error {e.code}: {e.message}")
```

## API Documentation

For detailed API documentation, please refer to the [Workiz API Documentation](https://api.workiz.com/api/v1/).

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.