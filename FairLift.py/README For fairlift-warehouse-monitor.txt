FairLift Warehouse - XAMPP ZIP
=============================

Files included:
- warehouse.php         -> Main dashboard (open in browser)
- db.php                -> Database connection (XAMPP defaults: root / no password)
- fetch_parcels.php     -> Returns JSON list of parcels
- add_parcel.php        -> Adds a parcel (expects JSON POST)
- update_status.php     -> Update parcel status (expects JSON POST)
- init.sql              -> SQL to create database + sample data
- README.txt            -> This file

Installation steps (local XAMPP):
1. Copy the extracted folder `fairlift_warehouse` into your XAMPP htdocs directory.
   Example: C:\xampp\htdocs\fairlift_warehouse\

2. Start Apache and MySQL via XAMPP control panel.

3. Import the database:
   - Go to http://localhost/phpmyadmin
   - Click 'Import' and import the included init.sql file, OR use the SQL tab to run its contents.

4. Open in browser:
   http://localhost/fairlift_warehouse/warehouse.php

Notes:
- db.php uses default XAMPP credentials (root with no password). Change db.php if your setup differs.
- This is a simple demo; for production, secure the PHP endpoints, validate input server-side, and add authentication.
