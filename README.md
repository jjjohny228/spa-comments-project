# Spa comments

## Installation

- Usage
1. Clone the repository:

```python
git clone https://github.com/jjjohny228/spa-comments-project.git
```

1. Go to the project directory:

```python
cd spa-comments-project
```

1. Create .env file in project. Use .env.exaple as a template.
2. To use S3, sign up on the [storj](https://eu1.storj.io/signup) site, create a bucket, and create secret keys.
3. Run docker compose file

```python
docker compose up --build
```

## **Features**

Users can leave comments with the following fields:

1. User Name (alphanumeric characters) - required field.
2. E-mail (email format) - required field.
3. Home page (URL format) - optional field.
4. CAPTCHA (alphanumeric characters) - image and required field.

The main page of the application has the following requirements:

1. Comments can have multiple replies (cascade display).
2. Top-level comments (not replies) are displayed in a table format with the ability to sort by the following fields: User Name, E-mail, and Date added (both in ascending and descending order).
3. Messages are paginated with 25 messages per page.

File Handling:

1. Users can add an image or a text file to their comment.

## **Technology Stack**

The project utilizes the following technologies and tools:

Backend:

1. Python programming language (OOP);
2. Django framework with the django-simple-captcha extension;
3. Postgresql database (Django Mttp).

Frontend:

1. HTML & CSS;
2. Bootstrap 5.

Git for version control.

Docker.