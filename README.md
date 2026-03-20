# Capstone one: Quick-Recipe

![img](/app/static/images/quick-recipe-logo.png)
## Unit 29 Capstone One

>To create a recipe recommendation system that utilizes free food APIs to suggest recipes to users based on their dietary restrictions, preferences, and available ingredients.
>**Host:** **[Render.com](https://render.com)**
>**The application is online at:**
>**https://quick-recipe.onrender.com**

![img](/app/static/images/quick-recipe-github-illustration.jpg)

**API**: **[Tasty (RAPID API)](https://rapidapi.com/apidojo/api/tasty)**

**DATABASE SCHEMA**:
![Img-Light](/documentations/database-schema-quick_recipe-white-bg.png#gh-light-mode-only)![Img-Dark](/documentations/database-schema-quick_recipe.png#gh-dark-mode-only)

## Application components:
This application has been created using the following components:
- **Python3** (version 3.11.1)
- **Flask** as a framework
- **Posgtres sql** as a Database

>**NB:**
>For this project I use Blueprint to organize the application.
That was a bit challenging because by using Blueprint everything wont work properly without additional configuration.

The rest of the components are available in the **pyproject.toml**

## Summary:

The main goal of this application is to create a recipe recommendation system that utilizes free food APIs to suggest recipes to users based on their dietary restrictions, preferences, and available ingredients.
But with the limitations of the features of API [Tasty (RAPID API)](https://rapidapi.com/apidojo/api/tasty) I could not achieved those features like the recommendation based on the dietary or ingredient. Instead I implemented the recommendations based on the user's preferences recipe save in the favorite recipes.

**Find below all the features implemented by this application:**

- **User's account:**

The application allows users to create an account to get access to certain features like **``print``**, **``add favorites``**, **``sharing``**.

For an account activation this application use email notification and send an activation link.
we have two types of authentication.
    - First one is to authenticate with your **email address** and **password**.
    - Second one is to authenticate with **Google**

All user can do all basic action in user's profile like edit password, edit personal information, delete accounts.
Users authenticated with the Google authentication can just delete their account.

- **Allow users to search for recipe:**

The API has a limit number of requests. So to solve this problem, I use caching and saving some data in Database.
Users can save their favorite recipes if they are authenticated.

- **Recipe recommendation**

The user will be able to see similar recipe in the favorites section
This favorite section is only available for authenticated users.

## Getting Started

### Prerequisites
- Python 3.11.1
- [uv](https://docs.astral.sh/uv/) (package manager)
- PostgreSQL

### Installation

1. Clone the repository and navigate to the project folder.

2. Install dependencies with uv:
    ```bash
    uv sync
    ```

3. Create a `.env` file at the project root with the following variables:
    ```
    SECRET_KEY=your_secret_key
    URL_SAFE_KEY=your_url_safe_key
    DATABASE_URL=postgresql:///quick_recipe_db
    API_KEY=your_tasty_api_key
    MAIL_SMTP=smtp.sendgrid.net
    MAIL_PORT=587
    MAIL_USERNAME=apikey
    MAIL_PASSWORD=your_sendgrid_api_key
    MAIL_SENDER=your_sender_email
    MAIL_SENDER_NAME=Quick Recipe
    GOOGLE_CLIENT_ID=your_google_client_id
    GOOGLE_CLIENT_SECRET=your_google_client_secret
    GOOGLE_PROJECT_ID=your_google_project_id
    GOOGLE_REDIRECT_URI_BASE=http://127.0.0.1:5000
    ```

### Running the app

```bash
uv run flask run
```

Or with gunicorn:

```bash
uv run gunicorn wsgi:app --bind 0.0.0.0:8000
```

### Managing dependencies

| Task | Command |
|------|---------|
| Add a package | `uv add <package>` |
| Remove a package | `uv remove <package>` |
| Sync dependencies | `uv sync` |
