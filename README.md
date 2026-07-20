# 🚦 TrafficEye - City Traffic Violation Log Analyzer & Dashboard

TrafficEye is a web-based Traffic Violation Management System developed using **Python, Django, and MongoDB**. The system helps traffic authorities manage traffic violations, monitor fine collections, generate reports, and maintain digital traffic records efficiently.

---

## 📌 Features

### 👤 User Authentication

- User Registration
- User Login
- Secure Logout
- Session-Based Authentication
- Protected Dashboard

### 🚔 Traffic Violation Management

- Add New Violation
- View All Violations
- Edit Violation Details
- Delete Violation
- Mark Fine as Paid

### 🔍 Search & Filter

- Search by Vehicle Number
- Search by Owner Name
- Filter by Violation Status
- Filter by Violation Type
- Sort by Newest/Oldest
- Pagination Support

### 📊 Reports

- Dashboard Statistics
- Daily Report
- Monthly Report
- Yearly Report
- Vehicle Report
- Officer Report
- Pending Fine Report
- Paid Fine Report

### 📁 Export

- Export Reports to CSV
- Export Reports to PDF

---

## 🛠️ Technologies Used

### Frontend

- HTML5
- CSS3
- Bootstrap 5
- JavaScript

### Backend

- Python
- Django

### Database

- MongoDB

### Libraries

- PyMongo
- ReportLab

---

## 📂 Project Structure

TrafficEye/
│
├── api/
├── database/
├── reports/
├── users/
├── violations/
├── templates/
├── static/
├── media/
├── config/
├── manage.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/TrafficEye.git
```

### 2. Go to Project Folder

```bash
cd TrafficEye
```

### 3. Create Virtual Environment

```bash
python -m venv venv
```

### 4. Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure MongoDB

Start MongoDB Server and update your MongoDB connection in:

```
database/mongodb.py
```

### 7. Run Project

```bash
python manage.py runserver
```

Open your browser:

```
http://127.0.0.1:8000/
```

---

## 📸 Screenshots

Add screenshots of:

- Home Page
- Login
- Register
- Dashboard
- Add Violation
- Violation List
- Reports
- CSV Export
- PDF Export

---

## 📊 Modules

### User Module

- Registration
- Login
- Logout
- Session Management

### Violation Module

- Add Violation
- Edit Violation
- Delete Violation
- Fine Payment
- Search
- Filter
- Pagination

### Report Module

- Dashboard
- Daily Report
- Monthly Report
- Yearly Report
- Vehicle Report
- Officer Report
- Pending Report
- Paid Report

---

## 🔒 Security Features

- Session-Based Authentication
- Protected Routes
- Input Validation
- MongoDB ObjectId Validation
- Invalid Request Handling

---

## 🚀 Future Enhancements

- Admin & Officer Roles
- Email Notifications
- SMS Alerts
- Payment Gateway Integration
- Traffic Analytics Dashboard
- Interactive Charts & Graphs
- AI-Based Traffic Violation Prediction
- REST API Integration
- Mobile Application

---

## 👨‍💻 Developed By

** Riteshkumar Badgujar**

Master of Computer Applications (MCA)

MET's Institute of Management Bhujbal Knowledge City, Nashik

---

## ⭐ If you like this project

Give this repository a ⭐ on GitHub.