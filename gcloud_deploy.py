#!/usr/bin/env python3
"""
This script deploys the Room8 app to Google Cloud App Engine and displays key details such as the target URL.
It also handles version management by deleting older versions if the number exceeds a set limit.
"""

import subprocess
import json
import time
import os
import sys
import random
import string

# Set the maximum versions value here
VERSION_MAX = 15
DEFAULT_SERVICE_NAME = "default"

print(f"You have chosen to keep {VERSION_MAX} versions of your app.")

# Function to get versions of a service
def get_versions(service_name):
    try:
        result = subprocess.run(
            ["gcloud", "app", "versions", "list", "--service", service_name, "--format", "json", "--project", PROJECT_ID],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        versions = json.loads(result.stdout)
        versions.sort(key=lambda x: x["version"]["createTime"], reverse=True)
        return versions
    except subprocess.CalledProcessError as e:
        if "Service not found" in e.stderr.decode():
            print(f"Service {service_name} not found. It will be created during deployment.")
            return []
        else:
            raise e

# Function to delete versions
def delete_versions(service_name, versions_to_delete):
    for v in versions_to_delete:
        version_id = v["id"]
        print(f"Deleting version {service_name}-{version_id}")
        subprocess.run(
            ["gcloud", "app", "versions", "delete", version_id, "--service", service_name, "--quiet", "--project", PROJECT_ID],
            check=True)

# Function to get changed files using git diff 
def get_changed_files(directory):
    """ Get list of new or modified files using git diff """
    try:
        result = subprocess.run(
            ["git", "-C", directory, "diff", "--name-only", "HEAD^", "HEAD"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        files = result.stdout.decode().strip().split("\n")
        return [os.path.join(directory, f) for f in files if f]
    except subprocess.CalledProcessError:
        print("Error determining changed files.")
        return []

# Function to generate a valid version name 
def generate_version_name():
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"version-{random_string}"

# Function to deploy the services
def deploy_service(service_name, yaml_path):
    start_time = time.time()
    current_directory = os.path.dirname(os.path.abspath(yaml_path))
    print(f"Deploying service: {service_name} using {yaml_path}")

    # List changed files
    print("Listing new or modified files to be uploaded to Google Cloud Storage:")
    changed_files = get_changed_files(current_directory)
    if changed_files:
        for file_path in changed_files:
            print(f"Changed file: {file_path}")
    else:
        print("No new or modified files detected.")
    
    # Check the current versions
    try:
        print(f"Getting current versions for service: {service_name}")
        versions = get_versions(service_name)
        print(f"{len(versions)} versions retrieved successfully.")
    except subprocess.CalledProcessError as e:
        versions = []
        print(f"Failed to get versions. Error: {e}")
        print(f"First deployment for service {service_name}. Proceeding with deployment.")
    
    print(f"You currently have {len(versions)} versions for {service_name}.")
    if versions:
        print(f"The latest version is {versions[0]['id']} for {service_name}.")
    
    if len(versions) > VERSION_MAX:
        print(f"More than {VERSION_MAX} versions exist for {service_name}.")
    
    # Deploy new version
    version_name = generate_version_name()
    print(f"Deploying new version: {version_name}")
    try:
        result = subprocess.run(
            ["gcloud", "app", "deploy", yaml_path, "--quiet", "--project", PROJECT_ID, "--version", version_name],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        print("Deployment output:", result.stdout.decode())
        print("Deployment done for", service_name)
    except subprocess.CalledProcessError as e:
        print("Failed to deploy new version. Error:", e.stderr.decode())
        return  # Early exit if deployment fails
    
    # After successful deployment, display the target URL
    print("\nDeployment Details:")
    print("---------------------------------------------------------")
    print(f"Target project:        {PROJECT_ID}")
    print(f"Target service:        {service_name}")
    print(f"Target version:        {version_name}")
    # Note: The target URL structure will be similar to below; adjust based on your region if needed.
    target_url = f"https://{PROJECT_ID}.wm.r.appspot.com"
    print(f"Target URL:            {target_url}")
    print("---------------------------------------------------------\n")
    
    # Delete old versions if needed
    if len(versions) > VERSION_MAX:
        try:
            versions_to_delete = versions[VERSION_MAX:]
            delete_versions(service_name, versions_to_delete)
            print(f"Deleted {len(versions_to_delete)} old versions.")
        except subprocess.CalledProcessError as e:
            print("Failed to delete old versions. Error:", e.stderr.decode())

    end_time = time.time()
    print(f"gCloud Script finished for {service_name}. Total execution time: {end_time - start_time} seconds.")

# Function to verify directory and gcloud project
def check_gcloud_project():
    current_dir = os.path.basename(os.getcwd())
    current_project = subprocess.run(
        ["gcloud", "config", "get-value", "project"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout.decode().strip()

    print(f"Current directory: {current_dir}")
    print(f"Current Google Cloud project: {current_project}")

    if current_dir not in current_project:
        print(f"Error: Current gcloud project is '{current_project}' but expected keyword '{current_dir}' in project name.")
        print("To switch projects, use: gcloud config set project <PROJECT_ID>")
        sys.exit(1)

    global PROJECT_ID
    PROJECT_ID = current_project
    print(f"Successfully authenticated to the correct Google Cloud project: {current_project}")

# Main deployment function
def main_deploy():
    check_gcloud_project()
    deploy_service(DEFAULT_SERVICE_NAME, 'app.yaml')
    print("\nTo tail logs for default, run: gcloud app logs tail -s default")

if __name__ == "__main__":
    main_deploy()