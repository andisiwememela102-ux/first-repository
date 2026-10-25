# Planning — eCommerce Application

## 1. System requirements

### User roles
- **Buyer:** register, log in/out, browse active products across stores, add/update/remove cart items, check out, view their invoice, and submit one review per product.
- **Vendor:** register, log in/out, create and manage their own stores, and add/edit/remove products in those stores.
- **Administrator:** use Django admin to manage users and application records.

### Main data
- A profile stores the user's role.
- A store belongs to one vendor.
- A product belongs to one store and has a price, stock count and active flag.
- A cart is stored in the user's Django session.
- An order and order items preserve the checkout and invoice details.
- A review belongs to a buyer and product; purchase history determines whether it is verified.
- Password reset tokens are stored as hashes with an expiry and used flag.

### Functional requirements
1. Account registration validates passwords using Django's password validators.
2. Authentication is handled by Django; anonymous users are redirected to login for protected actions.
3. Vendor management actions are limited to vendor accounts and objects owned by that vendor.
4. Checkout verifies product availability, updates stock in a database transaction, saves an invoice/order, clears the session cart, and emails invoice details where an email address is configured.
5. Reviews show verified status only if an order item exists for that buyer and product.
6. Password reset links expire after 15 minutes, are stored as hashes, and cannot be reused.
7. Database schema changes are tracked with Django migrations.

## 2. User interface plan
- A shared navigation bar links to Home, Stores and Cart, with login/register or logout depending on authentication state.
- Home shows available products and store names.
- Store pages show store information and its products; owners see store management links.
- Product pages show description, price, stock, cart controls and reviews.
- Cart displays quantity controls, line totals and the overall total before checkout.
- Checkout leads to a printable invoice page.
- Forms use clear labels, Django validation messages and CSRF protection.

## 3. Access control and data security
- Use Django's built-in authentication and password hashing rather than storing raw passwords.
- Require login for cart modifications, checkout, reviews and invoices.
- Restrict store/product write operations to vendor users and filter database lookups by the current owner.
- Use POST for destructive actions and logout, with CSRF tokens in forms.
- Validate prices, quantities, passwords and form input on the server.
- Use atomic checkout transactions to avoid partially completed orders; check stock again at checkout.
- Hash reset tokens before storing them, expire them quickly, and mark them used after reset.
- Keep secrets and database/email credentials in environment variables; never commit `.env`.
- Use HTTPS, `DEBUG=False`, a strong secret key and secure cookie settings in production.

## 4. Failure handling
- Invalid login displays a generic error without revealing which credential was wrong.
- Invalid form input is returned with validation messages and does not save the object.
- Attempts by buyers to access vendor management return HTTP 403; attempts to access another vendor's object return 404.
- Invalid quantities are normalised or rejected, and checkout checks the latest stock before changing inventory.
- Checkout is wrapped in a transaction so an unavailable product prevents a partial order.
- Empty carts cannot be checked out.
- Unknown, expired or already-used password reset tokens are rejected.
- Email delivery is configured to use the console backend for local development, allowing the link/invoice content to be inspected without real email credentials.
- Automated tests cover important role, cart, checkout and review scenarios.

## 5. Suggested manual acceptance checks
1. Register a vendor and create a store and product.
2. Register a buyer, browse the product and add a quantity to the cart.
3. Check out and confirm that an invoice is displayed, the cart is empty and stock decreased.
4. Review a purchased product and confirm it is marked verified; review a product without purchasing and confirm it is unverified.
5. Confirm a buyer cannot create or edit a store.
6. Request a password reset and check the development console for the 15-minute reset URL.
