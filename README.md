# Flask Inventory Management (MySQL, no ORM)

This is a simple Inventory Management web application built with Flask and MySQL **without** using SQLAlchemy (raw SQL via `mysql-connector-python`).

## What's included
- `app.py` - Flask application with routes for Products, Locations, Movements, and Report.
- `db_config.py` - Database connection function (please update credentials).
- `schema.sql` - SQL script to create `inventory_db` and tables.
- `templates/` - HTML templates (Jinja2).
- `static/style.css` - Minimal styling.
- `requirements.txt` - Python dependencies.

## Setup & Run

1. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate    # macOS/Linux
venv\Scripts\activate     # Windows (PowerShell/CMD)
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create the database and tables:
- Open MySQL client and run:
```sql
SOURCE schema.sql;
```
or run the commands in `schema.sql` manually.

4. Update `db_config.py`:
- Replace `user` and `password` with your MySQL credentials.

5. Run the app:
```bash
python app.py
```
Open `http://127.0.0.1:5000` in your browser.

## Notes
- You will need to create sample Products and Locations (3-4 each) and then create many ProductMovements to test the report.
- This project intentionally avoids using an ORM to demonstrate SQL skills.

Good luck on your hiring test! If you want, I can:
- Add sample data insertion SQL
- Create screenshots and a polished README with Git instructions