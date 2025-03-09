# EV-Charging-Management-System
EV Charging Management System is a web service that enables EV charging consumers to manage and monitor their charging remotely at ease.

---

## **Features**

- **User Authentication**:
  - Register and log in as a regular user or admin.
  - Admins can add, update, and view stations and transactions.
  - Regular users can view stations, manage chargers, and start/stop charging sessions.

- **Real-Time Charger Status**:
  - View real-time status updates for each charger (e.g., "Charging Started", "Charging Stopped").
  - WebSocket-based communication for real-time updates.

- **OCPP 1.6 Protocol**:
  - Supports OCPP 1.6 messages such as `BootNotification`, `Heartbeat`, `Authorize`, `StartTransaction`, and `StopTransaction`.

- **Database**:
  - Stores user data, stations, chargers, and transactions.
  - Uses PostgreSQL (or SQLite for development).

---

## **Technologies Used**

- **Backend**:
  - Django
  - Django Channels (for WebSocket support)
  - OCPP Python library (for OCPP 1.6 protocol)

- **Frontend**:
  - HTML, CSS, JavaScript
  - WebSocket API for real-time updates

- **Database**:
  - PostgreSQL (or SQLite for development)

---

## **Setup Instructions**

### **1. Clone the Repository**

```bash
git clone https://github.com/your-username/EV_charging_management_system.git
cd EV_charging_management_system
```

### **2. Install Dependencies**

```bash
pip install -r requirements.txt
```

### **3. Configure the Database**

#### 1- Update the database settings in settings.py:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ev_charging',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

#### 2-Run migrations:

```bash
python manage.py migrate
```

### **4. Create a Superuser**
Create an admin user to access the Django admin panel:
```bash
python manage.py createsuperuser
```

### **5. Run the Development Server**
Start the Django development server:

```bash
python manage.py runserver
```
Visit http://127.0.0.1:8000/ in your browser to access the application.

## **Testing with an OCPP Simulator**
1- Use an OCPP simulator (e.g., [MicroOcppSimulator](https://github.com/matth-x/MicroOcppSimulator)) to connect to the backend.
2- Send test requests (e.g., ==BootNotification==, ==Heartbeat==) and observe the logs and real-time updates in the frontend.

## **API Endpoints**

|Endpoint                               | Description                     |
|:--------------------------------------|:--------------------------------|
|/register/	                            | User registration               |
|/login/                                | User login                      |
|/logout/                               | User logout                     |
|/home/                                 | User or admin home page         |
|/add_station/                          | Add a new station (admin only)  |
|/update_station/<int:station_id>/	    | Update a station (admin only)   |
|/view_transactions/<int:station_id>/	| View transactions (admin only)  |
|/manage_charger/<int:charger_id>/	    | Manage a charger (user only)    |


## **WebSocket Endpoints*

|Endpoint                  | Description                           |
|:-------------------------|:--------------------------------------|
|/ws/charger/<charger_id>/ | Real-time communication with a charger|


## **Requirements**
- Python 3.8+
- PostgreSQL (or SQLite for development)
- Django 4.0+
- Django Channels
- OCPP Python library

## **Contributing**
1- Fork the repository.

2- Create a new branch (git checkout -b feature/your-feature).

3- Commit your changes (git commit -m 'Add some feature').

4- Push to the branch (git push origin feature/your-feature).

5- Open a pull request.

## **License**
This project is licensed under the MIT License. See the LICENSE file for details.

## **Contact**
For questions or feedback, please contact:

Sahar Aladdin - sahr.attallah@gmail.com

Project Repository - GitHub