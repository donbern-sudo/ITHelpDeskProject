from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3

# Create a Flask web application instance
app = Flask(__name__)

# Set a secret key for session handling and flash messages
app.secret_key = 'supersecurekey'

# ----------------------------
# ROUTES (PAGES) BEGIN HERE
# ----------------------------
sql_statement = """CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY, 
            name text NOT NULL, 
            email NOT NULL, 
            issue NOT NULL
        );"""

try:
    with sqlite3.connect('tickets.db') as conn:
        # create a cursor
        cursor = conn.cursor()

        # execute statements
        cursor.execute(sql_statement)

        # commit the changes
        conn.commit()

        print("Ticket table created successfully.")
except sqlite3.OperationalError as e:
    print("Failed to create ticket table:", e)
# Home page — Ticket submission form
@app.route('/')
def home():
    return render_template('home.html')
# Handle form submission from the home page
@app.route('/submit_ticket', methods=['POST'])
def submit_ticket():
    name = request.form['name']
    email = request.form['email']
    issue = request.form['issue']

    # Save the submitted ticket to the SQLite database
    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tickets (name, email, issue) VALUES (?, ?, ?)", (name, email, issue))
    conn.commit()
    conn.close()

    flash('✅ Ticket submitted successfully!')
    return redirect(url_for('home'))

# Admin login page
@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Replace this with secure credential management!
        if username == 'admin' and password == 'admin123':
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash('❌ Invalid login credentials')
            return redirect(url_for('admin_login'))

    return render_template('admin_login.html')

# Admin dashboard — View all submitted tickets
@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin'):
        flash('⛔ Unauthorized access')
        return redirect(url_for('admin_login'))

    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, issue FROM tickets")
    tickets = cursor.fetchall()
    conn.close()

    return render_template('admin_dashboard.html', tickets=tickets)

# Logout route for the admin
@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    flash('🔓 Logged out successfully.')
    return redirect(url_for('admin_login'))


if __name__ == "__main__":
    # Only run this if you're testing locally
    app.run(debug=True)
