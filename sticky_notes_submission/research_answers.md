# Research Answers

## 1. How HTTP applications preserve state across requests

HTTP is stateless, which means each request is handled independently and the server does not automatically remember what happened in an earlier request. Web applications preserve useful state by attaching a session identifier to the browser, usually in a cookie. With Django's default session setup, the browser stores the session ID while session data is stored on the server in the database. On later requests, Django's `SessionMiddleware` reads the cookie and makes the session available through `request.session`. The application can store small pieces of information there, such as a shopping cart or a temporary workflow value. Authentication builds on this mechanism: after a successful login, Django's authentication system records the user's ID in the session, and authentication middleware makes the logged-in user available as `request.user` on later requests. The application can then check `request.user.is_authenticated` before showing protected pages or allowing restricted actions. Sessions need sensible expiry settings, and cookies should be protected with secure settings when HTTPS is used. Login forms and state-changing requests should also use Django's CSRF protection. Session IDs and secret keys must be handled carefully because stolen or exposed credentials can allow unauthorised access. This approach lets a sequence of separate HTTP requests behave like one continuous user experience. See the official Django documentation on sessions and authentication.

Sources:
- https://docs.djangoproject.com/en/6.0/topics/http/sessions/
- https://docs.djangoproject.com/en/6.0/topics/auth/default/

## 2. Django migrations with a server-based database such as MariaDB

Django migrations record model changes as Python files and apply those changes to a database schema. To use MariaDB, first create a database and a database user with only the permissions the application needs, and ensure the database server is reachable from the application. Install a supported Python database driver; Django's MariaDB support uses its MySQL database backend. In `settings.py`, configure `DATABASES["default"]` with `ENGINE` set to `django.db.backends.mysql`, and provide the database name, username, password, host and port. Keep real production credentials outside source control, for example in environment variables. Before applying changes, back up important data and test migrations against a staging copy where possible. Run `python manage.py makemigrations` to generate migration files from model changes, inspect the generated files, and commit those migration files together with the model changes. Then run `python manage.py migrate` against the intended database to apply pending migrations. `python manage.py showmigrations` can help confirm which migrations have been applied, while `python manage.py sqlmigrate app_name migration_name` displays the SQL Django plans to run. After deployment, run `python manage.py check` and test the application's key database operations. MariaDB and MySQL do not provide the same transactional behaviour for every schema change as SQLite or PostgreSQL, so backups and careful deployment planning are important.

Sources:
- https://docs.djangoproject.com/en/6.0/ref/databases/
- https://docs.djangoproject.com/en/6.0/topics/migrations/
