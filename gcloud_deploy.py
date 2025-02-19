#!/usr/bin/env python3
"""
This script deploys the Room8 app to Google Cloud App Engine.
It also checks your current versions and deletes any older versions if the limit is exceeded.
"""

import subprocess
import json
import time
import os
import sys
import random
import string

# Configuration variables for Room8
VERSION_MAX = 15  # Maximum versions to keep
PROJECT_ID = "room8-oly"  # Your new Google Cloud project ID for Room8
DEFAULT_SERVICE_NAME = "default"  # Usually the default App Engine service

print(f"You have chosen to keep a maximum of {VERSION_MAX} versions of your app.")

def get_versions(service_name):
    try:
        result = subprocess.run(
            [
                "gcloud", "app", "versions", "list",
                "--service", service_name,
                "--format", "json",
                "--project", PROJECT_ID
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        versions = json.loads(result.stdout)
        # Sort versions by creation time (newest first)
        versions.sort(key=lambda x: x["version"]["createTime"], reverse=True)
        return versions
    except subprocess.CalledProcessError as e:
        stderr = e.stderr.decode()
        if "Service not found" in stderr:
            print(f"Service {service_name} not found. It will be created during deployment.")
            return []
        else:
            raise e

def delete_versions(service_name, versions_to_delete):
    for v in versions_to_delete:
        version_id = v["id"]
        print(f"Deleting version {service_name}-{version_id}")
        subprocess.run(
            [
                "gcloud", "app", "versions", "delete", version_id,
                "--service", service_name,
                "--quiet",
                "--project", PROJECT_ID
            ],
            check=True
        )

def get_changed_files(directory):
    try:
        result = subprocess.run(
            ["git", "-C", directory, "diff", "--name-only", "HEAD^", "HEAD"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        files = result.stdout.decode().strip().split("\n")
        return [os.path.join(directory, f) for f in files if f]
    except subprocess.CalledProcessError:
        print("Error determining changed files.")
        return []

def generate_version_name():
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"version-{random_string}"

def deploy_service(service_name, yaml_path):
    start_time = time.time()
    current_directory = os.path.dirname(os.path.abspath(yaml_path))
    print(f"Deploying service: {service_name} using {yaml_path}")
    
    changed_files = get_changed_files(current_directory)
    if changed_files:
        print("New or modified files:")
        for file_path in changed_files:
            print(file_path)
    else:
        print("No new or modified files detected.")
    
    # Retrieve current versions for the service
    try:
        versions = get_versions(service_name)
    except subprocess.CalledProcessError:
        versions = []
        print(f"First deployment for service {service_name}.")
    
    print(f"You currently have {len(versions)} versions for {service_name}.")
    if versions:
        print(f"The latest version is {versions[0]['id']}")

    if len(versions) >= VERSION_MAX:
        print(f"More than {VERSION_MAX} versions exist. New deployment will result in deletion of older versions after keeping {VERSION_MAX - 1} newest ones.")
    
    # Deploy a new version with a generated version name
    version_name = generate_version_name()
    print(f"Deploying new version: {version_name}")
    try:
        subprocess.run(
            [
                "gcloud", "app", "deploy", yaml_path,
                "--quiet",
                "--project", PROJECT_ID,
                "--version", version_name
            ],
            check=True
        )
        print(f"Deployment successful for service {service_name}.")
    except subprocess.CalledProcessError as e:
        print("Failed to deploy new version. Error:")
        print(e.stderr.decode())
        sys.exit(1)
    
    # Delete older versions if necessary
    if len(versions) >= VERSION_MAX:
        # Refresh the version list after deployment
        versions = get_versions(service_name)
        versions_to_delete = versions[VERSION_MAX - 1:]
        if versions_to_delete:
            delete_versions(service_name, versions_to_delete)
            print(f"Deleted {len(versions_to_delete)} old versions.")

    end_time = time.time()
    print(f"Deployment finished for {service_name}. Total execution time: {end_time - start_time} seconds.")

def main_deploy():
    deploy_service(DEFAULT_SERVICE_NAME, 'app.yaml')
    print("\nTo view live logs, run: gcloud app logs tail -s default")

if __name__ == "__main__":
    main_deploy()