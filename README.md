# Money Manager Application

## Description

The Money Manager Application is a Django-based web application designed to help users manage their personal finances efficiently. It allows users to track income, expenses, and savings using a secure and interactive platform.

## Key Features

- **Secure Authentication**: Implements email-based OTP verification for user authentication.
- **Financial Tracking**: Enables tracking of income, expenses, and savings.
- **Interactive Reports**: Utilizes Chart.js for dynamic financial visualizations.
- **Account Management**: Allows users to update account settings, including username, email, and password.
- **Email Notifications**: Configured using Gmail's SMTP server for verification and password resets.

## Technologies Used

- **Backend**: Django, Python
- **Frontend**: HTML, CSS, JavaScript, Chart.js
- **Database**: PostgreSQL

## Getting Started

### Prerequisites

- Python 3.x
- Django
- PostgreSQL

### Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/money-manager.git
    cd money-manager
    ```

2. **Set up a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure environment variables**:
   - Create a `.env` file in the project root directory with your email credentials and database settings.

5. **Run database migrations**:
    ```bash
    python manage.py migrate
    ```

6. **Start the server**:
    ```bash
    python manage.py runserver
    ```

## Usage

- Navigate to `http://localhost:8000` in your web browser.
- Register or log in to start managing your finances.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for review.
