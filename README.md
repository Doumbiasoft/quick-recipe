# Quick Recipe

![logo](/app/static/images/quick-recipe-logo.png)

> A recipe recommendation web application that lets users search, save, and share recipes using the [Tasty (RapidAPI)](https://rapidapi.com/apidojo/api/tasty) food API.

**Live:** [https://quick-recipe.doumbiasoft.com](https://quick-recipe.doumbiasoft.com)

![preview](/app/static/images/quick-recipe-github-illustration.jpg)

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Database Schema](#database-schema)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [Running the App](#running-the-app)
- [Managing Dependencies](#managing-dependencies)
- [API Reference](#api-reference)
- [Authentication](#authentication)
- [Email Notifications](#email-notifications)

---

## Features

- **Recipe Search** — Search recipes by name or filter by tags (vegetarian, desserts, gluten-free, etc.)
- **Recipe Details** — View full recipe details including ingredients, instructions, video and credits
- **Favorites (Pinning)** — Authenticated users can pin/unpin recipes to their favorites list
- **Recipe Recommendations** — Get similar recipe suggestions based on saved favorites
- **User Accounts** — Register with email/password or sign in with Google OAuth2
- **Account Activation** — Email-based account activation with a time-limited token link
- **Password Reset** — Email-based password reset flow with a time-limited token link
- **Social Sharing** — Share recipes on Facebook, Twitter and LinkedIn
- **Print** — Print-friendly recipe view
- **Admin Dashboard** — Admin users can view all registered subscribers
- **API Caching** — API responses cached locally for 12 weeks to reduce rate-limit consumption

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.13 |
| Framework | Flask 3.x |
| Database | PostgreSQL |
| ORM | SQLAlchemy 2.x |
| Auth | Flask-Bcrypt, Google OAuth2 (google-auth-oauthlib) |
| Forms | Flask-WTF, WTForms |
| Sessions | Flask-Session (filesystem) |
| Tokens | itsdangerous (URLSafeTimedSerializer) |
| Email | smtplib + SendGrid SMTP |
| API Caching | requests-cache |
| Templates | Jinja2 |
| WSGI Server | Gunicorn |
| Package Manager | [uv](https://docs.astral.sh/uv/) |

---

## Project Structure

```
capstone-one-quick-recipe/
├── app/
│   ├── __init__.py              # App factory
│   ├── extensions.py            # Extensions, constants, and utilities
│   ├── mailing.py               # Email sending logic
│   ├── auth/                    # Auth blueprint
│   │   ├── __init__.py
│   │   └── routes.py            # Login, register, OAuth, password reset
│   ├── main/                    # Main blueprint
│   │   ├── __init__.py
│   │   └── routes.py            # Home, favorites, user profile
│   ├── search/                  # Search blueprint
│   │   ├── __init__.py
│   │   └── routes.py            # Recipe search and details
│   ├── models/
│   │   ├── users.py             # User model
│   │   ├── recipe_favorites.py  # Saved recipes model
│   │   └── recipe_review.py     # Recipe reviews model
│   ├── forms/
│   │   ├── auth/
│   │   │   ├── login.py
│   │   │   └── register.py
│   │   └── search/
│   │       └── recipes.py
│   ├── templates/               # Jinja2 templates
│   ├── static/                  # CSS, JS, images, mail templates
│   └── cache/                   # Local API response cache
├── helpers.py                   # Caching session and utility functions
├── config.py                    # App configuration
├── wsgi.py                      # WSGI entry point with ProxyFix
├── pyproject.toml               # Project dependencies (uv)
├── Procfile                     # Production server command
└── .env                         # Environment variables (not committed)
```

---

## Database Schema

![Schema Light](/documentations/database-schema-quick_recipe-white-bg.png#gh-light-mode-only)
![Schema Dark](/documentations/database-schema-quick_recipe.png#gh-dark-mode-only)

### Models

#### User
| Column | Type | Description |
|--------|------|-------------|
| id | Integer PK | Auto-increment |
| first_name | String(255) | Required |
| last_name | String(255) | Required |
| email | String(50) | Unique, required |
| password | Text | Bcrypt hash |
| is_active | Boolean | False until email activation |
| is_admin | Boolean | Admin flag |
| is_oauth | Boolean | Google OAuth user flag |
| oauth_provider | Text | e.g. "Google" |
| oauth_uid | Text | OAuth unique identifier |
| oauth_profile_url | Text | Profile picture URL |
| created_at | DateTime | Auto |
| updated_at | DateTime | Auto |

#### RecipeFavorite
| Column | Type | Description |
|--------|------|-------------|
| id | Integer PK | Auto-increment |
| user_id | FK → users.id | Required |
| recipe_id | Integer | Tasty API recipe ID |
| name | Text | Recipe name |
| tag | Text | Recipe tag |
| thumbnail_url | Text | Thumbnail image URL |
| description | Text | Recipe description |
| data | JSONB | Full recipe data |
| created_at | DateTime | Auto |

#### RecipeReview
| Column | Type | Description |
|--------|------|-------------|
| id | Integer PK | Auto-increment |
| user_id | FK → users.id | Required |
| recipe_id | Integer | Tasty API recipe ID |
| comment | String(255) | Review text |
| rating | Float | Numeric rating |
| created_at | DateTime | Auto |

---

## Getting Started

### Prerequisites

- Python 3.13
- [uv](https://docs.astral.sh/uv/) — install with `curl -LsSf https://astral.sh/uv/install.sh | sh`
- PostgreSQL

### Installation

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd capstone-one-quick-recipe
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

3. Create the database:
   ```bash
   createdb quick_recipe_db
   ```

4. Set up your `.env` file (see [Environment Variables](#environment-variables)).

5. Initialize the database tables:
   ```bash
   uv run flask shell
   >>> from app.extensions import db
   >>> db.create_all()
   >>> exit()
   ```

---

## Environment Variables

Create a `.env` file at the project root:

```env
# App
SECRET_KEY=your_secret_key
URL_SAFE_KEY=your_url_safe_key

# Database
DATABASE_URL=postgresql:///quick_recipe_db

# Food API (Tasty via RapidAPI)
API_KEY=your_rapidapi_key
API_CACHE_WEEKS_TIMEOUT=12

# Email (SendGrid)
MAIL_SMTP=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USERNAME=apikey
MAIL_PASSWORD=your_sendgrid_api_key
MAIL_SENDER=noreply@yourdomain.com
MAIL_SENDER_NAME=Quick Recipe

# Google OAuth2
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_PROJECT_ID=your_google_project_id
GOOGLE_REDIRECT_URI_BASE=http://127.0.0.1:5000
```

---

## Running the App

**Development:**
```bash
uv run flask run
```

**Production:**
```bash
uv run gunicorn wsgi:app --bind 0.0.0.0:8000
```

---

## Managing Dependencies

| Task | Command |
|------|---------|
| Install all dependencies | `uv sync` |
| Add a package | `uv add <package>` |
| Remove a package | `uv remove <package>` |
| Upgrade all packages | `uv sync --upgrade` |

---

## API Reference

**Provider:** [Tasty (RapidAPI)](https://rapidapi.com/apidojo/api/tasty)

**Base URL:** `https://tasty.p.rapidapi.com`

| Endpoint | Usage |
|----------|-------|
| `GET /recipes/list` | Search and list recipes by name, tag, or random |
| `GET /tags/list` | Fetch all available tags for filtering |
| `GET /recipes/list-similarities` | Fetch similar recipes by recipe ID |

API responses are cached locally for 12 weeks to minimize rate-limit usage. The cache is stored at `app/cache/local_cache`.

---

## Authentication

### Email / Password

1. **Register** — Submit the registration form. A confirmation email with an activation link (valid 10 minutes) is sent.
2. **Activate** — Click the link in the email to activate the account.
3. **Login** — Submit email and password. Bcrypt is used to verify the password hash.
4. **Password Reset** — Request a reset email with a time-limited link (valid 2 minutes) to set a new password.

### Google OAuth2

1. Click **Sign in with Google**.
2. Authorize the app in Google's consent screen.
3. On callback, the app verifies the ID token and either logs in the existing user or creates a new account.
4. Google accounts cannot use the password reset flow.

> Note: An email already registered with a standard account cannot be used with Google OAuth, and vice versa.

---

## Email Notifications

Emails are sent via **SendGrid SMTP** using Python's `smtplib`. The following emails are sent automatically:

| Trigger | Email |
|---------|-------|
| New registration | Account activation link |
| Account activated | Welcome email |
| Google OAuth signup | Welcome email |
| Password reset request | Password reset link |

Both SSL (port 465) and STARTTLS (port 587) are supported, configured via `MAIL_PORT`.

---

## Routes Summary

### Auth (`/auth`)

| Route | Method | Description |
|-------|--------|-------------|
| `/auth/authentication` | GET, POST | Login / Register page |
| `/auth/google-login` | GET | Start Google OAuth flow |
| `/auth/google/callback` | GET | Google OAuth callback |
| `/auth/logout` | POST | Logout |
| `/auth/email-reset-password` | GET, POST | Request password reset |
| `/auth/reset-user-password/<token>` | GET, POST | Set new password |
| `/auth/account-activation/<token>` | GET | Activate account |
| `/auth/activation-notification` | GET | Activation pending page |
| `/auth/send-email-reset-notification` | GET | Reset email sent page |
| `/auth/link-expired` | GET | Token expired page |

### Main (`/`)

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Homepage with recipe categories |
| `/recipes/favorites` | GET | Saved recipes and suggestions |
| `/recipes/pin` | POST | Pin / unpin a recipe |
| `/user/profile` | GET | User profile |
| `/user/edit-info` | POST | Update name |
| `/user/check-current-pass` | POST | Verify current password |
| `/user/save-password` | POST | Update password |
| `/user/delete-account` | POST | Delete account |
| `/subscribers` | GET | Admin: list all users |

### Search (`/search`)

| Route | Method | Description |
|-------|--------|-------------|
| `/search/recipes` | GET, POST | Search and filter recipes |
| `/search/recipes-item` | POST | Store recipe in session |
| `/search/recipes/details` | GET | Recipe detail page |
