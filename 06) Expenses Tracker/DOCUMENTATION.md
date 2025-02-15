# Expense Tracker Documentation

## Project Overview
The Expense Tracker is a Django web application designed to help users track and manage their expenses. It provides features for:
- Adding new expenses
- Editing existing expenses
- Deleting expenses
- Viewing expense summaries (daily, weekly, monthly, yearly, and by category)

## Project Structure
```
mysite/
├── myapp/                # Main application
│   ├── migrations/        # Database migrations
│   ├── static/           # Static files (CSS, JS)
│   ├── templates/       # HTML templates
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py          # Expense form
│   ├── models.py         # Expense model
│   ├── tests.py
│   ├── urls.py           # Application URLs
│   └── views.py           # Application views
├── mysite/                # Project configuration
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py       # Project settings
│   ├── urls.py           # Main URLs
│   └── wsgi.py
├── db.sqlite3             # SQLite database
└── manage.py              # Django management script
```

## Settings Configuration
Key settings include:
- **Database**: SQLite (db.sqlite3)
- **Installed Apps**:
  - Django core apps
  - 'myapp' (Expense Tracker)
- **Static Files**:
  - STATIC_URL = 'static/'
  - STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
- **Security**:
  - DEBUG = True (for development)
  - SECRET_KEY = '...' (auto-generated)

## URL Routing
### Main Project URLs (mysite/urls.py)
- `/admin/`: Django admin interface
- `/`: Includes myapp URLs

### Application URLs (myapp/urls.py)
- `/`: Index page (list and add expenses)
- `/edit/<id>/`: Edit existing expense
- `/delete/<id>/`: Delete expense

## Models
### ExpensesModel
Fields:
- `name`: Expense description (CharField, max_length=100)
- `amount`: Expense amount (IntegerField)
- `category`: Expense category (CharField, max_length=100)
- `date`: Expense date (DateField, auto_now=True)

## Views
### Index View
- Displays all expenses
- Handles new expense creation
- Calculates:
  - Total expenses
  - Yearly expenses
  - Monthly expenses
  - Weekly expenses
  - Daily expenses
  - Expenses by category

### Edit View
- Displays form with existing expense data
- Handles expense updates

### Delete View
- Handles expense deletion
- Redirects to index page

## Forms
### ExpensesForm
Fields:
- Name (expense description)
- Amount (expense amount)
- Category (expense category)

## Static and Template Files
### Static Files
- CSS files for styling
- JavaScript files for interactivity

### Templates
- `index.html`: Main page with expense list and form
- `edit.html`: Edit expense page
- `base.html`: Base template for consistent layout

## Installation and Setup
1. Clone the repository
2. Create virtual environment: `python -m venv myenv`
3. Activate environment:
   - Windows: `myenv\Scripts\activate`
   - macOS/Linux: `source myenv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run migrations: `python manage.py migrate`
6. Create superuser: `python manage.py createsuperuser`
7. Run development server: `python manage.py runserver`

## Usage
1. Access the application at `http://localhost:8000`
2. Use the form to add new expenses
3. Click edit icon to modify existing expenses
4. Click delete icon to remove expenses
5. View expense summaries in various time periods and categories

## Contributing
1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m 'Add some feature'`
4. Push to branch: `git push origin feature-name`
5. Create pull request

## License
[MIT License](LICENSE)
