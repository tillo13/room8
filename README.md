# Room8

Welcome to the Room8 repository! This repository contains the source code for the Room8 Flask web application along with all the scripts and configuration files needed to deploy the app to Google Cloud App Engine. This document will explain the purpose of each file and provide setup, deployment, and maintenance instructions for novice users.

---

## Table of Contents

- [Overview](#overview)
- [Repository Structure](#repository-structure)
- [File Explanations](#file-explanations)
  - [Application Files](#application-files)
  - [Deployment Files](#deployment-files)
  - [Utility and Documentation Files](#utility-and-documentation-files)
- [Setup and Deployment](#setup-and-deployment)
- [Additional Changes](#additional-changes)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

Room8 is a Flask-based web application that serves as a demonstration project for deploying a Python web application to Google Cloud App Engine. This repository contains all the necessary files to build, deploy, and maintain the application. We also integrate GitHub for version control, and our deployment process is automated with helper scripts.

---

## Repository Structure

Below is a quick summary of the repository structure:
room8/ ├── app.py # Main Flask application ├── app.yaml # App Engine configuration file ├── requirements.txt # Python dependencies list ├── templates/ │ ├── base.html # Base HTML template for consistent layout │ └── home.html # Home page extending base.html ├── static/ │ └── css/ │ └── style.css # Basic CSS styles for the application ├── git_push.sh # Shell script to commit/push code and deploy using gcloud_deploy.py ├── gcloud_deploy.py # Python script to deploy the app to Google Cloud App Engine and manage versions ├── .gcloudignore # File to specify files to ignore for deployment ├── how_we_build.md # A guide documenting the build and deployment process (see Additional Changes section for updates) └── README.md # This detailed documentation file

---

## File Explanations

### Application Files

- **`app.py`**  
  The main Flask application file. This file imports Flask, sets up route handlers, and runs the application. It renders templates stored in the `templates/` folder.

- **`templates/base.html` & `templates/home.html`**  
  The HTML templates for the app.

  - `base.html` defines the common structure (header, footer, etc.).
  - `home.html` extends `base.html` and includes custom content for the home page.

- **`static/css/style.css`**  
  Contains the CSS styles that control the look and feel of the application.

### Deployment Files

- **`app.yaml`**  
  The configuration file for Google App Engine. This file defines:

  - The Python runtime (currently using `python39`)
  - The entrypoint (to run the app with Gunicorn)
  - Handlers (rules for serving static content and routing requests)

- **`requirements.txt`**  
  Lists all the Python packages needed to run the application. This ensures that when the app is deployed, all dependencies are installed.

### Utility and Documentation Files

- **`git_push.sh`**  
   A shell script that automates the process of adding code changes to Git, committing them with a message, pushing them to GitHub, and then deploying the updated version to Google Cloud App Engine.  
   _Usage:_
  ```sh
  ./git_push.sh "your commit message"
  gcloud_deploy.py
  A Python script that:
  ```

Deploys the Room8 application using Google Cloud SDK
Generates a unique version name for the deployment
Manages old versions (deleting them when there are more than a set limit)
This script is called by git_push.sh after pushing your changes.
.gcloudignore
Lists files and directories that should be ignored during the deployment process to keep the deployment package lean.

how_we_build.md
A document detailing the entire build and deployment process. It includes steps for setting up the project, creating configurations, and attaching billing, as well as any additional changes (such as configuration and permission updates).

## Setup and Deployment

Setup
Clone the Repository:

If you haven’t already cloned the repository, run:

git clone https://github.com/yourusername/room8.git
cd room8
Create a Virtual Environment & Install Dependencies:

Create and activate a virtual environment (optional but recommended):

python3 -m venv venv
source venv/bin/activate
Install required packages:

pip install -r requirements.txt

## Google Cloud Project Setup:

Ensure you have the Google Cloud SDK installed.
Run gcloud init to create a new configuration for Room8, select your account, and create a new project (e.g., room8-oly).
Attach a billing account to your project in the Google Cloud Console.
Create the App Engine application by running:
gcloud app create
Deployment
To deploy the app:

Make your code changes.
Run the following command:
./git_push.sh "your commit message"
This script will:
Commit and push your changes to GitHub.
Invoke the deployment script to deploy the changes to Google Cloud App Engine.
After deployment, check the output for the target URL (e.g., https://room8-oly.wm.r.appspot.com) and open it in your browser.
Additional Changes
Refer to the "Additional Changes" section at the bottom of the how_we_build.md file for updates related to app.yaml changes and permission updates.

Troubleshooting
Deployment Issues:
If deployment errors occur, review the error messages in your terminal. Common issues include missing permissions or configuration errors.

Permissions:
Ensure that the service account (room8-oly@appspot.gserviceaccount.com) has the required roles (e.g., Storage Admin) as described in the Deployment documentation.

Log Viewing:
Use gcloud app logs tail -s default to view live application logs for debugging.

Contributing
Contributions to this repository are welcome! Please fork the repository, make your changes, and open a pull request with a detailed description of your changes.

License
This project is licensed under the MIT License. Please see the LICENSE file for details.
