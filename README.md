# Vendor Management System

## Video Demo

Link : https://drive.google.com/file/d/1BOdJfl1tgX8Z5uKgtZjfvZgPIiv9-pba/view?usp=drive_link

## API Reference

#### Vendor Profile Management:

```http
  POST /api/vendors/: Create a new vendor.
  GET /api/vendors/: List all vendors.
  GET /api/vendors/{vendor_id}/: Retrieve a specific vendor's details.
  PUT /api/vendors/{vendor_id}/: Update a vendor's details.
  DELETE /api/vendors/{vendor_id}/: Delete a vendor.
```


#### Purchase Order Tracking:

```http
  POST /api/purchase_orders/: Create a purchase order.
  GET /api/purchase_orders/: List all purchase orders with an option to filter by vendor.
  GET /api/purchase_orders/{po_id}/: Retrieve details of a specific purchase order.
  PUT /api/purchase_orders/{po_id}/: Update a purchase order.
  DELETE /api/purchase_orders/{po_id}/: Delete a purchase order.
```


#### Historical Performance:

```http
  GET /api/vendors/{vendor_id}/performance
```

## Tech Stack

**Stack:** Python, Django, dbsqlite3

**Server:** localhost:8000


## Installation

```bash

git clone https://github.com/dugu0011/VendorManagement.git
open VendorManagement into vs code

python -m venv venv

source venv/Scripts/activate (windows) or source venv/bin/activate (mac )

cd vendor_management_project

pip install -r requirements.txt or pip3 install -r requirements.txt

python manage.py makemigrations  or python3 manage.py makemigrations

python manage.py migrate or python3 manage.py migrate

python manage.py createsuperuser or python3 manage.py createsuperuser 

python manage.py runserver or python3 manage.py runserver

http://localhost:8000/api/  --for api swagger

http://localhost:8000/admin  --for admin
```



