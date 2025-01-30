# Food Consumption Tracker Documentation

## Introduction
This application is a Django-based project designed to help users track their food consumption. Users can register, log their food intake, and manage their consumption records.

### Technologies Used
- Django
- Python

## Installation Instructions
1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv myenv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```bash
     myenv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source myenv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration
The main configuration settings for the application can be found in the `mysite/mysite/settings.py` file. Important configurations include:
- **Database:** The application uses SQLite by default.
- **Installed Apps:** Ensure that `myapp` is included in the `INSTALLED_APPS` list.

## Running the Application
To run the application, use the following command:
```bash
python manage.py runserver
```
This will start the development server, and you can access the application at `http://127.0.0.1:8000/`.

## User Registration
To register a new user:
1. Navigate to the registration page at `/register/`.
2. Fill out the registration form and submit.

## Logging Food Consumption
As an authenticated user, you can log your food consumption:
1. Go to the home page.
2. Select the food item you consumed and submit the form.

## Deleting Consumption Records
To delete a food consumption record:
1. Navigate to the delete page for the specific record.
2. Confirm the deletion.

## URL Routing
The application has the following URL patterns:
- `/admin/`: Admin interface.
- `/`: Home page (food logging).
- `/register/`: User registration.
- `/delete/<int:id>`: Delete food consumption record.
- `/login/`: User login.
- `/logout/`: User logout.

## Conclusion
This documentation provides an overview of the Food Consumption Tracker application. For further information, refer to the [Django documentation](https://docs.djangoproject.com/en/5.1/).
