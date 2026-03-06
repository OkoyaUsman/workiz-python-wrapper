"""Example usage of the Workiz Python wrapper."""

from workiz import WorkizClient

# Initialize the client
# Replace with your actual API credentials
client = WorkizClient(
    api_token="your_api_token_here",
    auth_secret="your_auth_secret_here"
)

# Example: Get all jobs
print("Fetching jobs...")
try:
    jobs = client.jobs.all(start_date="2024-01-01", records=10)
    print(f"Found {len(jobs)} jobs")
    for job in jobs[:3]:  # Print first 3
        print(f"  - Job UUID: {job.get('UUID')}, Company: {job.get('Company')}")
except Exception as e:
    print(f"Error fetching jobs: {e}")

# Example: Get a specific job
print("\nFetching specific job...")
try:
    # Replace with actual UUID
    job = client.jobs.get("job-uuid-here")
    print(f"Job details: {job}")
except Exception as e:
    print(f"Error fetching job: {e}")

# Example: Get all leads
print("\nFetching leads...")
try:
    leads = client.leads.all(start_date="2024-01-01", records=10)
    print(f"Found {len(leads)} leads")
except Exception as e:
    print(f"Error fetching leads: {e}")

# Example: Get team members
print("\nFetching team members...")
try:
    team_members = client.team.all()
    print(f"Found {len(team_members)} team members")
    for member in team_members[:3]:  # Print first 3
        print(f"  - {member.get('name')} ({member.get('email')})")
except Exception as e:
    print(f"Error fetching team: {e}")

# Example: Get time off
print("\nFetching time off...")
try:
    time_offs = client.timeoff.get_all(all=True)
    print(f"Found {len(time_offs)} time off entries")
except Exception as e:
    print(f"Error fetching time off: {e}")