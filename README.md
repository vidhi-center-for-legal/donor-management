
# Donor Management System

Welcome to the Donor Management System developed by Tech4Good Community. This system leverages the capabilities of Frappe, ERPNext, and Payments to provide organizations with a comprehensive solution for managing donors and donations effectively.
# Features:
1. Leads Management
2. Agent Management
3. Tranche (or) Donation Tracking
4. Overall Donation Details
5. Utilisation Tracking
6. Reports on Tranche, Donation and Overall Donation
7. Lead Dashboard
8. Donation and Utilisation Dashboard
9. Donor Dashboard   
# Dependencies
To set up the Donor Management System, you'll need the following dependencies:

1.  Frappe Framework: A full-stack web application framework built with Python and JavaScript. It provides the foundation for building and customizing web applications.
2.  ERPNext: An open-source ERP system built on Frappe Framework, offering modules for managing various aspects of business operations.
3.  Payments App: An app integrated with ERPNext to handle payment processing and transactions related to donations

# Prerequisites for Installing Frappe Framework on VM
Before installing Frappe Framework on your virtual machine (VM), ensure that you have the following prerequisites:

- Operating System: Ubuntu 22.04 LTS
- Python: Version 3.10
- Node.js: Version 21.0 or higher.
- MariaDB: Version 10.6
- Redis: Version 5.x or higher.

# Installation
Installing Frappe Framework: Frappe Version 16

1. Install Prerequisites
- sudo apt update
- sudo apt install git python-dev python-pip redis-server
- sudo apt install software-properties-common
- sudo apt-get update
- sudo apt install -y mariadb-server mariadb-client
- mysql_secure_installation
    - Enter current password for root: (Enter your SSH root user password)
    - Switch to unix_socket authentication [Y/n]: Y
    - Change the root password? [Y/n]: Y
    - Remove anonymous users? [Y/n] Y
    - Disallow root login remotely? [Y/n]: N
    - Remove test database and access to it? [Y/n]: Y
    - Reload privilege tables now? [Y/n]: Y

- sudo apt install curl
- sudo curl https://raw.githubusercontent.com/creationix/nvm/master/install.sh | bash
- nvm install 21
- node -v
- sudo apt-get install npm
- npm install -g yarn
- apt-get install xvfb libfontconfig wkhtmltopdf
- sudo pip3 install frappe-bench

2. Creating Site and Installing the applications:
- bench new-site [site_name]
- bench get-app payments
- bench get-app erpnext
- bench --site [site_name] install-app payments
- bench --site [site_name] install-app erpnext
- bench get-app 'URL for Donor Management System'
- bench --site [site_name] install-app donor_management

# Installation on Frappe Cloud:
- checkout the following video for the reference to install apps on frappe cloud https://youtu.be/GeEiskWLf2k?si=b533oUm4oWk92kTa

# API Details 
- API 1: To generate Token for authentication
    - Method: GET
    - End Point: https://[DNS]/api/method/donor_management.donor_management.donor_api.get_token_api
- API 2: To send the donor and donation details to donor management app
    - Method: POST
    - End Point: https://[DNS]/api/method/donor_management.donor_management.donor_api.send_donation_data
- Before Using the APIs, the system manager must add details in  Udhyam Website API Settings Doc : 
    1. username
    2. password
    3. time period for token expiration
    4. Secret key 
    5. Check the Enable Api Access Checkbox.
- After Adding these records, The system manager will save the document.
- Sample data: 
    - username: udhyam
    - password: password123
    - Token Expiry Time (mins): 10
    - Secret Key: 71D59859F81E74569FE95B5C64C4B
- Postman Collection Link:
    - https://api.postman.com/collections/27116056-5269c52c-f2ea-4b02-b5bf-d8cad56fc731?access_key=PMAT-01HXE0CRSC7733K5911ZSF2T7B