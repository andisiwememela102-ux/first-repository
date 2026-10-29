# MarketPlace — Django eCommerce Application (Part 1)

MarketPlace is a learning project built with Django. It supports buyer and vendor accounts, vendor-owned stores and products, a session-based shopping cart, checkout and invoice records, product reviews, and password-reset links. Checkout records an order and updates inventory; it does **not** collect card payments.

## Features

- Buyer/vendor registration with case-insensitive duplicate-email validation.
- Role-aware navigation and access control: vendors manage their own stores/products; buyers shop and manage their own reviews.
- Product catalogue, store pages, stock-aware cart, a visible **Continue Shopping** link, and checkout.
- Order and invoice records, inventory updates, and invoice email (console output by default).
- Multiple reviews per buyer/product over time, same-day duplicate review prevention, and review edit/delete controls for the review's author.
- Verified-purchase labels, single-use expiring password-reset tokens, Django admin, and automated tests.
- SQLite by default, with optional MariaDB/MySQL configuration.

## Requirements

- Python 3.10 or newer (Python 3.11 or 3.12 recommended).
- Git, for cloning the project from your GitHub repository.
- Internet access during the first dependency installation.

## Publish the project to your personal GitHub repository (one-time prerequisite)

Create a repository on GitHub (for example, `django-marketplace`). Do not add a database file or a virtual environment to the repository. From the project folder, run:

```powershell
git init
git add .
git commit -m "Complete Django marketplace application"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/django-marketplace.git
git push -u origin main
```

Replace `YOUR-USERNAME` and `django-marketplace` with your GitHub username and repository name. If the project is already a Git repository with a remote, do not run `git init` or add a second remote; use `git remote -v` to check the existing remote.


## Step-by-step setup — Windows

### 1. Clone the project and enter its folder

Open PowerShell in the directory where you want the project saved. Replace the placeholder values with your own repository details:

```powershell
git clone https://github.com/YOUR-USERNAME/django-marketplace.git
cd django-marketplace
```

If your repository has a different name, use that name in the `cd` command. All commands below must be run from the folder containing `manage.py`.

### 2. Create and activate a virtual environment

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use Command Prompt instead:

```bat
.venv\Scripts\activate.bat
```

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

The default setup uses SQLite and does not require a separate database server. The MySQL driver is optional and is not needed for SQLite. Install Django directly for the default SQLite setup:

```powershell
python -m pip install "Django>=5.2,<6.0"
```

### 4. Create your local environment file

The repository includes `.env.example` as a reference. Copy it to `.env` if you want to keep local configuration values in one place:

```powershell
Copy-Item .env.example .env
```

Django's settings currently read configuration from environment variables; they do not automatically load `.env`. For the default SQLite/console-email setup, no environment variables are required. Never commit real passwords, API keys, or production secret keys. The `.env` file is ignored by Git, while `.env.example` is intentionally tracked as a safe template.

### 5. Set up the database and check the project

```powershell
python manage.py migrate
python manage.py check
python manage.py test
```

The migration creates the database schema. The SQLite database (`db.sqlite3`) is generated locally and must not be committed to GitHub. If you have a database from an older version of the project, the migration that allows multiple reviews will be applied automatically by `migrate`.

### 6. Create an administrator (optional)

```powershell
python manage.py createsuperuser
```

Follow the prompts. The admin site is available at `http://127.0.0.1:8000/admin/` after the server starts.

### 7. Start the development server

```powershell
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser. Stop the server with `Ctrl+C` in the terminal.

## How to test the buyer and vendor workflows

1. Register a new account and choose **Vendor**.
2. Select **Create store**, enter the store details, and save.
3. Open the store and choose **Add product**. Enter a name, description, positive price, and stock quantity.
4. Log out and register a second account with the **Buyer** role and a different email address.
5. Browse the home page or **Stores**, open a product, select a quantity, and choose **Add to cart**.
6. In the cart, try **Continue Shopping** to return to the catalogue and add another product. Return to the cart and choose **Checkout** to create an order and invoice.
7. Open the product page while logged in as the buyer and submit a review. You can edit or delete your own reviews. A buyer may submit another review for the same product on a later day.
8. To test access restrictions, sign in as a vendor and confirm that the buyer-only Cart navigation option is not shown.

By default, email messages (including invoices and password-reset links) are printed in the runserver terminal. This lets you test the flows without sending real emails.

## Optional MariaDB/MySQL setup

Install and configure MariaDB/MySQL, then install the optional Python driver. From the project folder, run `python -m pip install mysqlclient`. Set the following environment variables in your shell to match a database and user you created:

```text
DB_ENGINE=mysql
DB_NAME=ecommerce_db
DB_USER=ecommerce_user
DB_PASSWORD=your-local-database-password
DB_HOST=127.0.0.1
DB_PORT=3306
```

Then run `python manage.py migrate`. Keep real credentials outside the repository. SQLite remains the recommended option for a quick local review and automated tests.

## Run the tests

```powershell
python manage.py test
```

The tests cover product listing, role-based access, cart navigation, checkout behaviour, stock updates, duplicate-email rejection, and review verification/editing/deletion. Test results should finish with `OK`; investigate any reported failure before submitting.

## Project structure

```text
ecommerce_submission/
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
├── ecommerce_project/       # Django settings and root URLs
├── shop/                    # Models, forms, views, templates, tests, migrations
├── Planning/                # Requirements, design and acceptance checklist
└── docs/                    # Practical task research notes
```

## Git hygiene and submission checklist

- Commit source code, templates, migrations, tests, documentation, `requirements.txt`, and `.env.example`.
- Do **not** commit `db.sqlite3`, other database files, `.env`, `.venv/`, `venv/`, `__pycache__/`, or generated bytecode. These are covered by `.gitignore`.
- After making changes, use `git status`, run the checks and tests, then commit and push the finished work.

## Production considerations

This is an educational project, not a production-ready payment platform. Before deployment, configure a strong secret key, `DEBUG=False`, valid allowed hosts, HTTPS and secure cookie settings, production email, database backups, monitoring, and appropriate payment processing if required.
