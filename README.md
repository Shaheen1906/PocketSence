# **PocketSense**

**PocketSense** is a platform designed to help college students track and split their daily expenses with friends. The platform focuses on managing shared costs for everything from dining hall meals to textbooks, local travel, and weekend outings, making it easier to handle group expenses during college life.

---

## **Features**

### **Core Features**
1. **Expense Recording and Splitting**:
   - Record expenses and split them equally or unequally among group members.
2. **Group Management**:
   - Create and manage groups for shared expenses (e.g., hostel roommates, project teams, trip groups).
3. **Settlement Tracking**:
   - Track payments between users and manage pending settlements.
4. **Monthly Analysis**:
   - Analyze monthly spending and generate reports.
5. **Payment Reminders**:
   - Send reminders for pending settlements.

### **Advanced Features**
1. **Settlement Suggestions**:
   - Suggest optimal settlements based on net balances.
2. **Monthly Budget Tracking**:
   - Track monthly budgets and compare them with actual spending.


---

## **Technologies Used**

- **Backend**: Django, Django REST Framework (DRF)
- **Database**: PostgreSQL
- **Authentication**: JWT (JSON Web Tokens)
- **API Documentation**: Swagger/OpenAPI
- **Other Libraries**:
  - `psycopg2`: PostgreSQL adapter for Python
  - `django-filter`: For filtering API results
  - `drf-yasg`: For Swagger documentation

---

## **Setup Instructions**

### **1. Prerequisites**
- Python 3.8 or higher
- PostgreSQL
- pip (Python package manager)

### **2. Clone the Repository**
```bash
git clone https://github.com/your-username/pocketsense.git
cd pocketsense
```

### **3. Set Up a Virtual Environment**
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On Linux/macOS
```

### **4. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **5. Set Up PostgreSQL**
1. Create a database named `pocketsense` in PostgreSQL.
2. Update the `DATABASES` configuration in `settings.py` with your PostgreSQL credentials:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'pocketsense',
           'USER': 'your_db_user',
           'PASSWORD': 'your_db_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

### **6. Run Migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

### **7. Create a Superuser**
```bash
python manage.py createsuperuser
```

### **8. Run the Development Server**
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to access the application.

---

## **API Documentation**

The API documentation is available using Swagger/OpenAPI. After running the development server, visit:
```
http://127.0.0.1:8000/swagger/
```

---

## **API Endpoints**

### **Authentication**
- **Login**: `POST /login/`
  - Body:
    ```json
    {
        "username": "your_username",
        "password": "your_password"
    }
    ```

### **Students**
- **Create Student**: `POST /students/`
  - Body:
    ```json
    {
        "username": "user1",
        "password": "password123",
        "college": "ABC College",
        "semester": 3,
        "default_payment_method": "UPI",
        "upi_id": "user1@upi"
    }
    ```

### **Groups**
- **Create Group**: `POST /groups/`
  - Body:
    ```json
    {
        "name": "Roommates",
        "members": [1, 2]
    }
    ```

### **Expenses**
- **Create Expense**: `POST /expenses/`
  - Body:
    ```json
    {
        "amount": 100,
        "category": 1,
        "split_type": "EQUAL",
        "date": "2023-10-01",
        "paid_by": 1,
        "group": 1
    }
    ```
- **Create Expense With UnEqual Amount**: `POST /expenses/`
  - Body:
    ```json
    {
        "amount": 100,
        "category": 1,
        "split_type": "UNEQUAL",
        "split_details": {
            "2": 40,  
            "3": 60 
        },
        "date": "2023-10-01",
        "paid_by": 1,
        "group": 1
    }
    ```

### **Settlements**
- **Create Settlement**: `POST /settlements/`
This will Automatically manage while creating Expenses.
  - Body:
    ```json
    {
        "expense": 1,
        "payer": 2,
        "payee": 1,
        "amount": 50,
        "settlement_method": "UPI",
        "due_date": "2023-10-10"
    }
    ```

### **Monthly Analysis**
- **Get Monthly Analysis**: `GET /monthly-analysis/?date=YYYY-MM`
  - Example:
    ```
    GET /api/monthly-analysis/?date=2023-10
    ```

### **Settlement Suggestions**
- **Get Settlement Suggestions**: `GET /api/settlement-suggestions/?group_id=1`
  - Example:
    ```
    GET /api/settlement-suggestions/?group_id=1
    ```

