
# Authentication API Project

This project provides a RESTful API for user authentication and password management using Django Rest Framework (DRF) and JWT (JSON Web Token) authentication. It includes features such as login, logout, password reset, and password change.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Environment Configuration](#environment-configuration)
- [Running the Project](#running-the-project)
- [API Documentation](#api-documentation)
  - [1. Login Endpoint](#1-login-endpoint)
  - [2. Logout Endpoint](#2-logout-endpoint)
  - [3. Password Reset Request Endpoint](#3-password-reset-request-endpoint)
  - [4. Password Reset Confirmation Endpoint](#4-password-reset-confirmation-endpoint)
  - [5. Change Password Endpoint](#5-change-password-endpoint)
- [Running Tests](#running-tests)
- [Contributing](#contributing)
- [License](#license)

## Features

- **User Login**: Authenticate users with their username and password to obtain a JWT token.
- **User Logout**: Invalidate JWT tokens to log users out securely.
- **Password Reset**: Allow users to reset their password via an email link.
- **Password Change**: Enable authenticated users to change their password.

## Prerequisites

Before you begin, ensure you have the following installed on your local machine:

- Python 3.x
- Django
- Django Rest Framework
- PostgreSQL or any other preferred database

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/yourusername/authentication-api.git
   cd authentication-api
   ```

2. **Create and Activate a Virtual Environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scriptsctivate`
   ```

3. **Install Required Packages**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run Migrations**:

   ```bash
   python manage.py migrate
   ```

5. **Create a Superuser** (optional but recommended for admin access):

   ```bash
   python manage.py createsuperuser
   ```

## Environment Configuration

Create a `.env` file in the root directory of your project and configure the following environment variables:

```env
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgres://user:password@localhost:5432/yourdbname
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password
DEFAULT_FROM_EMAIL=your-email@example.com
```

Replace the placeholder values with your actual settings.

## Running the Project

1. **Start the Django Development Server**:

   ```bash
   python manage.py runserver
   ```

2. **Access the API**:

   Open your browser and go to `http://127.0.0.1:8000/` to access the API.

## API Documentation

### 1. **Login Endpoint**

- **URL**: `/api/login/`
- **Method**: `POST`
- **Description**: Authenticates a user and returns an authentication token.

#### Request Body

```json
{
  "username": "string",
  "password": "string"
}
```

#### Responses

- **200 OK**: User authenticated successfully.
  ```json
  {
    "token": "string"
  }
  ```
- **400 Bad Request**: Invalid credentials provided.
  ```json
  {
    "non_field_errors": ["Unable to log in with provided credentials."]
  }
  ```

### 2. **Logout Endpoint**

- **URL**: `/api/logout/`
- **Method**: `POST`
- **Description**: Logs out the user by invalidating the authentication token.

#### Request Headers

- **Authorization**: `Bearer <token>`

#### Responses

- **200 OK**: User logged out successfully.
  ```json
  {
    "message": "Successfully logged out."
  }
  ```
- **401 Unauthorized**: The user is not authenticated.
  ```json
  {
    "detail": "Authentication credentials were not provided."
  }
  ```

### 3. **Password Reset Request Endpoint**

- **URL**: `/api/password-reset-request/`
- **Method**: `POST`
- **Description**: Requests a password reset by sending an email with a reset link.

#### Request Body

```json
{
  "email": "string"
}
```

#### Responses

- **200 OK**: Password reset email sent.
  ```json
  {
    "message": "Password reset link sent."
  }
  ```
- **400 Bad Request**: Invalid email provided.
  ```json
  {
    "email": ["There is no user registered with this email address."]
  }
  ```

### 4. **Password Reset Confirmation Endpoint**

- **URL**: `/api/password-reset-confirm/`
- **Method**: `POST`
- **Description**: Resets the user's password using a token sent to their email.

#### Request Body

```json
{
  "uidb64": "string",
  "token": "string",
  "new_password": "string",
  "confirm_password": "string"
}
```

#### Responses

- **200 OK**: Password reset successfully.
  ```json
  {
    "message": "Password has been reset successfully."
  }
  ```
- **400 Bad Request**: Invalid token or mismatched passwords.
  ```json
  {
    "non_field_errors": ["Passwords do not match."],
    "token": ["Invalid or expired token."]
  }
  ```

### 5. **Change Password Endpoint**

- **URL**: `/api/change-password/`
- **Method**: `POST`
- **Description**: Allows an authenticated user to change their password.

#### Request Headers

- **Authorization**: `Bearer <token>`

#### Request Body

```json
{
  "old_password": "string",
  "new_password": "string",
  "confirm_password": "string"
}
```

#### Responses

- **200 OK**: Password changed successfully.
  ```json
  {
    "message": "Password updated successfully."
  }
  ```
- **400 Bad Request**: Old password is incorrect or new passwords do not match.
  ```json
  {
    "old_password": ["Old password is not correct."],
    "non_field_errors": ["The new passwords do not match."]
  }
  ```
- **401 Unauthorized**: The user is not authenticated.
  ```json
  {
    "detail": "Authentication credentials were not provided."
  }
  ```

## Running Tests

To run the tests for this project, use the following command:

```bash
python manage.py test
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an Issue.

## License

This project is licensed under the MIT License.
