
# Growthness API

This project provides a RESTful API using Django Rest Framework (DRF) and JWT (JSON Web Token) authentication. It includes features such as user authentication and password management, CRUD opeations for Habits, Goals, Achievements and more.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Environment Configuration](#environment-configuration)
- [Running the Project](#running-the-project)
- [API Documentation](#api-documentation)
  - [1. User Registration Endpoint](#1-user-registration-endpoint)
  - [2. Login Endpoint](#2-login-endpoint)
  - [3. Token Refresh Endpoint](#3-token-refresh-endpoint)
  - [4. Logout Endpoint](#4-logout-endpoint)
  - [5. Password Reset Request Endpoint](#5-password-reset-request-endpoint)
  - [6. Password Reset Confirmation Endpoint](#6-password-reset-confirmation-endpoint)
  - [7. Change Password Endpoint](#7-change-password-endpoint)
- [Running Tests](#running-tests)

## Features

- **User Registration**: Create new users with their username, email and password.
- **User Login**: Authenticate users with their username and password to obtain a JWT token.
- **User Logout**: Invalidate JWT tokens to log users out securely.
- **Password Reset**: Allow users to reset their password via an email link.
- **Password Change**: Enable authenticated users to change their password.

## Prerequisites

Before you begin, ensure you have the following installed on your local machine:

- Docker
- Docker Compose

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/MicaelTargino/Growthness.git growthness_api
   cd growthness_api
   ```

2. **Build the Docker Images**:

   ```bash
   docker-compose build
   ```

## Environment Configuration

Create a `.env` file in the root directory of your project and configure the following environment variables:

```env
SECRET_KEY=your_secret_key

SENDER_MAIL=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password (or app password)

FRONTEND_URL=http://localhost:3000/

POSTGRES_DB=your_database_name
POSTGRES_USER=your_database_user
POSTGRES_PASSWORD=your_database_password
```

Replace the placeholder values with your actual settings.

## Running the Project

1. **Start the Docker Containers**:

   ```bash
   docker-compose up
   ```

2. **Apply Migrations**:

   After the containers are running, open another terminal and run:

   ```bash
   docker-compose exec growthness_api python manage.py migrate
   ```

3. **Create a Superuser** (optional but recommended for admin access):

   ```bash
   docker-compose exec growthness_api python manage.py createsuperuser
   ```

4. **Access the API**:

   Open your browser and go to `http://127.0.0.1:8000/` to access the API.

## API Documentation

### 1. **User Registration Endpoint**

- **URL**: `/auth/register/`
- **Method**: `POST`
- **Description**: Registers a new user with the provided username, email, and password.

#### Request Body

```json
{
  "username": "string",
  "email": "string",
  "password": "string",
  "password2": "string"
}
```

#### Responses

- **201 Created**: User registered successfully.
  ```json
  {
    "message": "User registered successfully"
  }
  ```
- **400 Bad Request**: Invalid data provided.
  ```json
  {
    "username": ["This field is required."],
    "email": ["Enter a valid email address."],
    "password": ["This field is required."],
    "password2": ["Passwords do not match."]
  }
  ```

### 2. **Login Endpoint**

- **URL**: `/auth/token/`
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
    "refresh": "string",
    "access": "string"
  }
  ```
- **401 Unauthorized**: Invalid credentials provided.
  ```json
  {
    "detail": "No active account found with the given credentials."
  }
  ```

### 3. **Token Refresh Endpoint**

- **URL**: `/auth/token/refresh/`
- **Method**: `POST`
- **Description**: Refreshes the JWT token for authenticated users.

#### Request Body

```json
{
  "refresh": "string"
}
```

#### Responses

- **200 OK**: Token refreshed successfully.
  ```json
  {
    "access": "string"
  }
  ```
- **401 Unauthorized**: Invalid refresh token provided.
  ```json
  {
    "detail": "Token is invalid or expired."
  }
  ```

### 4. **Logout Endpoint**

- **URL**: `/auth/logout/`
- **Method**: `POST`
- **Description**: Logs out the user by invalidating the refresh token.

#### Request Headers

- **Authorization**: `Bearer <access_token>`

#### Request Body

```json
{
  "refresh_token": "string"
}
```

#### Responses

- **205 Reset Content**: User logged out successfully.
- **400 Bad Request**: Invalid refresh token provided.
  ```json
  {
    "detail": "Token is invalid or expired."
  }
  ```
- **401 Unauthorized**: The user is not authenticated.
  ```json
  {
    "detail": "Authentication credentials were not provided."
  }
  ```

### 5. **Password Reset Request Endpoint**

- **URL**: `/auth/password-reset-request/`
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

### 6. **Password Reset Confirmation Endpoint**

- **URL**: `/auth/password-reset-confirm/`
- **Method**: `POST`
- **Description**: Resets the user's password using a token sent to their email.

#### Request Body

```json
{
  "new_password": "string",
  "confirm_password": "string",
  "uid": "string",
  "token": "string"
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

### 7. **Change Password Endpoint**

- **URL**: `/auth/change-password/`
- **Method**: `POST`
- **Description**: Allows an authenticated user to change their password.

#### Request Headers

- **Authorization**: `Bearer <access_token>`

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
docker-compose exec growthness_api python manage.py test
```
