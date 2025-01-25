# Video Streaming Platform

A simple video streaming platform built with Flask that allows admin users to upload and manage videos, while visitors can watch the uploaded content.

## Features

- User authentication (Admin login)
- Video upload functionality for admins
- Video streaming capabilities
- Responsive design using Bootstrap
- SQLite database for storing video information

## Setup Instructions

1. Install Python 3.8 or higher if you haven't already.

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Access the website at `http://localhost:5000`

## Default Admin Credentials
- Username: admin
- Password: admin123

## Important Notes

- Videos are stored in the `static/uploads` directory
- Make sure to change the secret key in `app.py` before deploying to production
- The application uses SQLite by default, but you can configure it to use other databases
- For production deployment, consider using a proper web server like Nginx and a production-grade database

## Future Improvements

- User registration system
- Video categories and tags
- User comments and ratings
- Video quality selection
- Thumbnail generation
- Advanced admin dashboard
