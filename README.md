# Room8

Welcome to the Room8 repository! This repository contains the source code for the Room8 Flask web application along with scripts and configuration files for deploying the app to Google Cloud App Engine. This document explains the purpose of each file and provides setup, deployment, and maintenance instructions (designed for novice users).

---

## Table of Contents

- [Overview](#overview)
- [Repository Structure](#repository-structure)
- [File Explanations](#file-explanations)
  - [Application Files](#application-files)
  - [Deployment Files](#deployment-files)
  - [Utility and Documentation Files](#utility-and-documentation-files)
- [New Features](#new-features)
- [Setup and Deployment](#setup-and-deployment)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

Room8 is a Flask-based web application designed to help users find the ideal roommate while also demonstrating automated deployment to Google Cloud App Engine. The repository now includes new routes and templates (such as a login page and a more detailed roommate finder) plus utility scripts for deployment and project maintenance.

---

## Repository Structure

room8/ ├── app.py # Main Flask application, now includes routes for home, find_room8, mission, how_it_works, and login ├── app.yaml # App Engine configuration file ├── requirements.txt # Python dependencies list ├── static/ │ └── css/ │ └── style.css # CSS styles for the application ├── templates/ │ ├── base.html # Base HTML template for a consistent layout │ ├── home.html # Home page template │ ├── find_room8.html # New page for the Room8 finder function │ ├── mission.html # Page detailing the mission of Room8 │ ├── how_it_works.html # Explains how the Room8 app works │ └── login.html # New login page template for user authentication ├── utilities/ │ └── gmail_utils.py # Utility script for sending emails and managing Gmail interactions ├── gather_directory.py # Utility script to scan and gather file details in the project ├── gcloud_deploy.py # Script to deploy the app to Google Cloud App Engine and manage versions ├── how_we_setup.md # How-to guide for setting up and deploying the Room8 app └── README.md # This documentation file

---

## File Explanations

### Application Files

- **`app.py`**  
  Contains the main Flask application. It sets up the following routes:

  - `/` (Home): Renders the home page (`home.html`).
  - `/find_room8`: A form page where users can answer questions to find a compatible roommate.
  - `/mission`: A page explaining the app’s mission.
  - `/how_it_works`: Details how the application’s matching process works.
  - `/login`: A new login page that, once extended, will process user credentials.

- **Templates (`templates/` folder)**

  - **`base.html`**  
    The layout template that includes a fixed navbar (with links to Home, Mission, How It Works, Find a Room8, and Login) and a footer.
  - **`home.html`**  
    Extends `base.html` to display the home page content.
  - **`find_room8.html`**  
    A page that includes a form with questions to help find the ideal roommate.
  - **`mission.html`**  
    Explains the mission and core values behind Room8.
  - **`how_it_works.html`**  
    Provides a step-by-step explanation of the matching process.
  - **`login.html`**  
    A new page for logging in. Currently, it displays a simple form and a toast notification on submission.

- **Static Files**
  - **`static/css/style.css`**  
    Contains CSS reset rules and styles for layout, typography, and UI elements such as the navbar, hero section, buttons, and footer.

### Deployment Files

- **`app.yaml`**  
  The configuration file for Google App Engine. It defines:

  - The supported Python runtime (python39)
  - The entry point used by Gunicorn to serve the app
  - Handlers for serving static content and routing all other URLs to the application.

- **`requirements.txt`**  
  Lists all Python dependencies. This ensures the correct packages are installed during deployment.

- **`gcloud_deploy.py`**  
  A Python script that:
  - Checks the current Google Cloud project.
  - Retrieves and manages App Engine versions.
  - Deploys the app using a unique version and, if necessary, deletes older versions.

### Utility and Documentation Files

- **`utilities/gmail_utils.py`**  
  Provides functions for sending plain text and HTML emails, creating sample files, replying to emails, and reading emails from Gmail. It uses environment variables for Gmail credentials.

- **`gather_directory.py`**  
  Scans the entire project directory (excluding certain folders) and gathers a list of files and directories. The result is written to a timestamped file for maintenance or review purposes.

- **`how_we_setup.md`**  
  A detailed guide on creating a GitHub repository, setting up local development, configuring Google Cloud, and deploying the Room8 app.

---

## New Features

- **Login Functionality:**  
  A new `/login` route and corresponding template have been added. While the back-end processing (such as verifying user credentials) is not yet fully implemented, the login page provides a user interface for future authentication functionality.

- **Additional Templates:**  
  Besides the standard home page, new pages such as `find_room8.html`, `mission.html`, `how_it_works.html`, and `login.html` have been added to provide a richer and more comprehensive user experience.

- **Utility for Directory Gathering:**  
  The script `gather_directory.py` now automates the process of gathering all relevant files and directories (excluding common ignored folders). This is useful for creating documentation or maintenance reports.

- **Enhanced Deployment Script:**  
  The deployment script `gcloud_deploy.py` manages version control and deployment details including deleting older versions after a set limit is exceeded.

---

## Setup and Deployment

1. **Clone the Repository:**

   ```sh
   git clone https://github.com/yourusername/room8.git
   cd room8
   Set Up Your Virtual Environment and Install Dependencies:
   ```

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
Configure Google Cloud:

Install the Google Cloud SDK.

Run gcloud init and follow the prompts to set up your Google account and create a new project (e.g., room8-oly).

Attach a billing account to your project via the Google Cloud Console.

Create the App Engine application by running:

gcloud app create
Deploy the Application:

Run the deployment script by executing:

python gcloud_deploy.py
After deployment, note the printed target URL (for example, https://room8-oly.wm.r.appspot.com) and open it in your browser.

Monitoring Logs:

To tail live logs for troubleshooting or monitoring, run:

gcloud app logs tail -s default
Troubleshooting
Deployment Issues:
Check your terminal output for error messages. Common problems include missing permissions or configuration issues with your Google Cloud project.

Permissions:
Ensure that the service account (e.g., room8-oly@appspot.gserviceaccount.com) has the required roles such as Storage Admin. For example, use:

gcloud projects add-iam-policy-binding room8-oly \
 --member="serviceAccount:room8-oly@appspot.gserviceaccount.com" \
 --role="roles/storage.admin"
Mail Sending Issues:
If emails are not sent, double-check the environment variables set in your .env file for ROOM8_GMAIL_USERNAME and ROOM8_GMAIL_APP_PASSWORD.

Contributing
Contributions are welcome! If you’d like to improve Room8, please follow these steps:

Fork this repository.
Create a new branch with your changes (git checkout -b feature/my-feature).
Commit your changes (git commit -m "Add my feature").
Push to your branch (git push origin feature/my-feature).
Open a pull request with a clear description of your changes.
License
This project is licensed under the MIT License. See the LICENSE file for details.
