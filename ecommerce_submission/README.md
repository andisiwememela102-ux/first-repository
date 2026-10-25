# Django MarketPlace — eCommerce Application (Part 1)

A modular Django eCommerce application for vendor and buyer accounts. Vendors manage their own stores and inventory; buyers browse products, use a session-based cart, check out, receive an invoice email, and leave product reviews. Reviews are marked verified when the buyer has an order containing the product. The project also includes time-limited password-reset links.

## Features
- Registration and login with buyer/vendor roles; logout uses POST.
- Vendor-only store and product create/edit/delete actions, scoped to the owning vendor.
- Product catalogue, stock validation, session cart, checkout and invoice records.
- Invoice email via Django's configured email backend.
- Verified/unverified reviews and one review per buyer/product.
- Password reset tokens hashed in the database, single-use and expiring after 15 minutes.
- Django admin, automated tests and database configuration for SQLite (default) or MariaDB/MySQL.


## Project layout
- `ecommerce_project/` — project settings and URL configuration.
- `shop/` — models, forms, views, templates, admin registration and tests.
- `Planning/` — requirements, interface, security and failure-handling plan.
- `docs/practical_task_2_research.md` — research notes for the second practical task.
