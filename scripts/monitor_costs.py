"""
Monitors AWS costs for a specified time period.

This function uses the AWS Cost Explorer API to retrieve the total unblended cost
for the specified time period. The results are printed to the console.

Note:
    The time period is currently hardcoded to start on June 1, 2025, and end on June 15, 2025.
    Ensure that the AWS credentials are properly configured in your environment.

Dependencies:
    - boto3: AWS SDK for Python

Raises:
    KeyError: If the response structure does not contain the expected keys.
    boto3.exceptions.Boto3Error: If there is an issue with the AWS API request.

Example:
    >>> monitor_aws_costs()
    AWS Total cost: 123.45
"""
import sys

import boto3


def monitor_aws_costs():
    client = boto3.client("ce")
    response = client.get_cost_and_usage(
        TimePeriod={"Start": "2025-06-01", "End": "2025-06-15"}
    )
    total_cost = response["ResultsByTime"][0]["Total"]["UnblendedCost"]["Amount"]
    print(f"AWS Total cost: {total_cost}")


def monitor_gcp_costs():
    # Placeholder for GCP cost management API
    print("GCP cost monitoring not implemented")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python monitor_costs.py <cloud-provider>")
        sys.exit(1)
    if sys.argv[1] == "aws":
        monitor_aws_costs()
    elif sys.argv[1] == "gcp":
        monitor_gcp_costs()
