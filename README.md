# Rental Listing Platform

A full-stack rental listing aggregation platform that collects housing listings from multiple rental sources and displays them through a centralized web application.

The goal of the project is to make it easier for students and renters to browse rental opportunities without having to manually search across multiple housing websites.

## Features

- Aggregates rental listings from multiple sources
- Scrapes rental information from:
  - The Cannon
  - Places4Students
- Displays listings through a responsive web interface
- Search and filtering functionality
- Displays rental information such as:
  - Price
  - Bedrooms
  - Bathrooms
  - Description
  - Utilities information
  - Listing source
- Links users to the original rental listing
- Removes duplicate listings based on their source URL
- Supports automated scraping through GitHub Actions
- REST API built with Django REST Framework
- Next.js frontend connected to the Django backend

## Tech Stack

### Frontend

- Next.js
- React
- TypeScript
- CSS

### Backend

- Python
- Django
- Django REST Framework
- django-filter
- django-cors-headers

### Web Scraping & Data Processing

- BeautifulSoup
- Requests
- Pandas
- Regular Expressions

### Database

- SQLite for local development
- PostgreSQL / Supabase support

### Development & Automation

- Git
- GitHub
- GitHub Actions
- npm
- Concurrently

## Project Structure

```text
Rental-Listing-Platform/
│
├── backend/
│   ├── api/
│   │   └── Django REST API
│   │
│   ├── collectors/
│   │   ├── the_cannon.py
│   │   └── places4students.py
│   │
│   ├── main/
│   │   └── Django project configuration
│   │
│   ├── manage.py
│   ├── run_scraper.py
│   └── requirements.txt
│
├── frontend/
│   ├── app/
│   ├── public/
│   └── package.json
│
├── .github/
│   └── workflows/
│       └── scrape.yml
│
├── .gitignore
├── package.json
├── package-lock.json
└── README.md
```

## How It Works

The application collects rental listings from supported housing websites and makes them available through one interface.

```text
The Cannon ────────────┐
                       │
Places4Students ───────┤
                       ↓
                 Python Scrapers
                       ↓
                  Data Processing
                       ↓
                   Django API
                       ↓
                Next.js Frontend
                       ↓
                     User
```

The scrapers extract listing information such as price, description, bedrooms, bathrooms, utilities, images, and links to the original property.

Pandas is used to combine the collected data and remove duplicate listings.

The Django backend exposes the rental data through a REST API, which is consumed by the Next.js frontend.

## Running the Project Locally

### 1. Clone the repository

```bash
git clone https://github.com/Jkhaleed/-Rental-Listing-Platform.git
cd Rental-Listing-Platform
```

### 2. Set up the Django backend

Navigate to the backend:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

Run database migrations:

```bash
python manage.py migrate
```

Return to the project root:

```bash
cd ..
```

### 3. Set up the Next.js frontend

```bash
cd frontend
npm install
cd ..
```

### 4. Install root development dependencies

From the project root:

```bash
npm install
```

### 5. Start the full application

```bash
npm run dev
```

This starts both the Next.js frontend and Django backend.

The frontend is typically available at:

```text
http://localhost:3000
```

The Django development server is typically available at:

```text
http://127.0.0.1:8000
```

## Running the Web Scraper

Activate the backend virtual environment and run:

```bash
cd backend
python run_scraper.py
```

The scraper collects listings from the supported rental sources and processes the results.

## Automated Web Scraping

GitHub Actions is being used to automate the rental listing collection process.

The workflow is located at:

```text
.github/workflows/scrape.yml
```

The workflow can be configured to periodically:

1. Check out the repository
2. Set up Python
3. Install backend dependencies
4. Run the rental listing scraper
5. Update the generated listing data

This allows the listing dataset to be refreshed without manually running the scraper.

## Environment Variables

Sensitive information is stored using environment variables and is not committed to the repository.

For local backend development, create:

```text
backend/.env
```

Environment variables may include database configuration and other application secrets.

Frontend environment variables can be stored in:

```text
frontend/.env.local
```

For example:

```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

## Current Development Status

The core full-stack application is functional locally.

Completed:

- [x] Next.js frontend
- [x] Django backend
- [x] Django REST API
- [x] The Cannon scraper
- [x] Places4Students scraper
- [x] Combined rental listing dataset
- [x] Duplicate listing removal
- [x] Frontend/backend integration
- [x] Single-command local development with `npm run dev`
- [x] GitHub repository setup
- [x] GitHub Actions workflow setup
- [x] Project structure cleanup

In progress:

- [ ] Improve detection of expired rental listings
- [ ] Complete and verify scheduled GitHub Actions scraping
- [ ] Improve scraper reliability
- [ ] Production deployment
- [ ] Production database configuration
- [ ] Additional frontend polish

## Future Improvements

Planned improvements include:

- Automatically remove expired rental listings
- Add additional rental listing sources
- Improve search and filtering
- Add price sorting
- Add pagination
- Improve listing image handling
- Add loading and error states
- Add location-based filtering
- Improve mobile responsiveness
- Deploy the Django API
- Deploy the Next.js frontend
- Automatically synchronize scraped listings with the production database

## Purpose

This project was built to practice and demonstrate full-stack software development, including:

- Frontend development with React and Next.js
- Backend API development with Django
- REST API integration
- Web scraping
- Data processing
- Database integration
- Git and GitHub workflows
- Development automation
- Full-stack application architecture

## Author

**Khaleed Jimoh**

Computer Engineering — University of Guelph

GitHub: [Jkhaleed](https://github.com/Jkhaleed)
