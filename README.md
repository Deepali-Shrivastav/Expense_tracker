# 💸 Expense Tracker

A modern, user-friendly web application built with **Django** to help users track and manage their expenses efficiently, with powerful features such as interest tracking, long-term planning, and interactive visualizations using Plotly.

## 🚀 Features

### 🔐 User Authentication

- Secure user registration & login system
- Custom user creation form with simplified password validation
- Session-based authentication with toast notifications
- Personalized welcome messages on login
- Secure logout functionality

### 💼 Expense Management

- Add, edit, and delete both **regular** and **long-term expenses**
- Categorize expenses by **date**, **type**, and **interest rate**
- Long-term expense support:

  - Interest rate & end date tracking
  - Automatic duration-based cost calculations

### 📊 Dashboard & Analytics

- Interactive monthly expense graph using **Plotly.js**
- Organized expense list grouped by month
- Responsive, clean dashboard interface
- Real-time form validation and feedback

### 🎨 UI & Visual Features

- Modern, sticky navigation bar with branding
- Grid-based, responsive layout
- Interactive toast notifications for user feedback
- Font Awesome icons for visual clarity
- Consistent color scheme & elegant typography

## ⚙️ Tech Stack

### 🔧 Backend

- Python 3.x
- Django 4.x
- SQLite database

### 🖥️ Frontend

- HTML5
- CSS3 (with custom properties/variables)
- JavaScript (ES6+)
- jQuery for DOM interactions
- Plotly.js for charts
- Font Awesome 5

### 📦 Libraries & Packages

- `django-crispy-forms` – Enhanced form rendering
- `plotly` – Interactive graphs
- `django.contrib.auth` – Built-in authentication

## 🧩 Project Structure

```
expense_tracker/
├── exp_tracker/
│   ├── static/
│   │   └── css/
│   │       ├── styles.css         # General styles
│   │       ├── home.css           # Dashboard-specific styles
│   │       └── login_styles.css   # Authentication page styles
│   ├── templates/
│   │   ├── base.html              # Main layout
│   │   ├── home/                  # Home page templates
│   │   ├── registration/          # Auth-related templates
│   │   └── exp_tracker/           # App-specific templates
│   ├── forms.py                   # Form definitions
│   ├── models.py                  # Expense models
│   ├── urls.py                    # URL routes
│   └── views.py                   # View logic
├── manage.py                      # Django CLI
├── requirements.txt               # Python dependencies
└── README.md                      # README
```

## 🔧 Installation & Setup

Follow these steps to run the project locally:

### 1. Clone the Repository

```bash
git clone https://github.com/Deepali-Shrivastav/Expense_tracker.git
cd Expense_tracker
```

### 2. Create & Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Migrations

```bash
python manage.py migrate
```

### 5. Create a Superuser (Admin)

```bash
python manage.py createsuperuser
```

> You'll be prompted to enter a username, email, and password.

### 6. Run the Development Server

```bash
python manage.py runserver
```

Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) to use the app.
Visit [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) to access the admin dashboard.

## 🧪 Usage Instructions

1. **Register** with your email and password
2. **Login** to your personalized dashboard
3. **Add expenses** via the form:

   - Regular: name, amount, date
   - Long-term: name, amount, interest rate, end date

4. **View your data**:

   - Interactive monthly graph (Plotly)
   - Monthly grouped list of expenses
   - Total and interest-adjusted values

## 💡 Design Highlights

### 📱 Responsive Layout

- Mobile-first, grid-based design
- Adaptive resizing for various devices

### 🎨 Color Scheme

- **Primary**: `#4f46e5` (Indigo)
- **Text**: `#1f2937` (Dark Gray)
- **Background**: `#f9fafb` (Light Gray)
- **Cards**: `#ffffff` (White)

### ✍️ Typography

- **Font**: 'Inter', sans-serif
- Consistent spacing, hierarchy & readability

## 🔒 Security Features

- CSRF protection
- Hashed passwords & secure form processing
- Session-based access control
- Protected views and routes
- Validated & sanitized form inputs

## 🌱 Future Enhancements

- Expense export to CSV/PDF
- Category-wise tracking
- Budget goal setting & alerts
- Expense analytics & reports
- Multi-currency support
- Receipt image uploads
- Shared/group expenses
