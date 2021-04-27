import json
import sqlite3
from models import User

def get_all_users():
    # Open a connection to the database
    with sqlite3.connect("./rare.db") as conn:
        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            u.id,
            u.first_name,
            u.last_name,
            u.email,
            u.bio,
            u.username,
            u.password,
            u.profile_image_url,
            u.created_on,
            u.active
        FROM Users u
        """)

        # Initialize an empty list to hold all animal representations
        users = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            user = User(row['id'], row['first_name'], row['last_name'],
                            row['email'], row['bio'],
                            row['username'], row['password'], row['profile_image_url'], row['created_on'], row['active'])

            users.append(user.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(users)

def get_single_user(id):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            u.id,
            u.first_name,
            u.last_name,
            u.email,
            u.bio,
            u.username
        FROM Users u
        WHERE u.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()

        user = User(data['id'], data['first_name'], data['last_name'],
                            data['email'], data['bio'],
                            data['username'])

        return json.dumps(user.__dict__)

def create_user(new_user):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Users
            ( first_name, last_name, email, bio, username, password, profile_image_url, active )
        VALUES
            ( ?, ?, ?, ?, ?, ?, ?, ? );
        """, (new_user['first_name'], new_user['last_name'],
              new_user['email'], new_user['bio'],
              new_user['username'],new_user['password'],
              new_user['profile_image_url'], new_user['active']))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_user['id'] = id


    return json.dumps(new_user)