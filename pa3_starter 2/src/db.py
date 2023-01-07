import sqlite3

# From: https://goo.gl/YzypOI
def singleton(cls):
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return getinstance


class DatabaseDriver(object):
    """
    Database driver for the Venmo (Full) app.
    Handles with reading and writing data with the database.
    """

    def __init__(self):
        """
        secures a connection with the database and stores it into the instance
        variable 'conn'
        """
        self.conn = sqlite3.connect(
            "todo.db", check_same_thread=False
        )
        self.delete_user_table()
        self.create_user_table()
        self.create_exchange_table()

# Users tables

    def create_user_table(self):
        """
        Using SQL, creates a user table
        """
        self.conn.execute(
            """
            CREATE TABLE user(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            username TEXT NOT NULL,
            balance INTEGER NOT NULL
        );
        """)

    def delete_user_table(self):
        """
        Using SQL, delete the user table
        """
        self.conn.execute("DROP TABLE IF EXISTS user;")

    def get_all_users(self):
        cursor = self.conn.execute("SELECT * FROM user")
        users = []
        for row in cursor:
            users.append({"id": row[0], "name": row[1], "username": row[2]})
        return users

    def insert_user_table(self, name, username, balance):
        """
        Using SQL, inserts a user into the user table
        """
        cursor = self.conn.execute("INSERT INTO user (name, username, balance) VALUES(?,?,?);", (name, username, balance))

        self.conn.commit()
        return cursor.lastrowid

    def get_user_by_id(self, id):
        """
        Using SQL, gets a user by its id
        """
        cursor = self.conn.execute("SELECT * FROM user WHERE id =?;", (id,))

        for row in cursor:
            return {"id": row[0], "name": row[1], "username": row[2], "balance": row[3]}

        return None

    def delete_user_by_id(self, id):
        """
        Using SQL, deletes a user from a table
        """

        self.conn.execute("DELETE FROM user WHERE id = ?;", (id,))
        self.conn.commit()

# Exchanges Tables

    def create_exchange_table(self):
        """
        Using SQL, create a exchange table
        """
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS exchange (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp INTEGER,
                sender_id INTEGER NOT NULL,
                receiver_id INTEGER NOT NULL,
                amount INTEGER NOT NULL,
                message TEXT,
                accepted BOOLEAN,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES user(id)
            );
            """
        )

    def insert_exchange(self, sender_id, receiver_id, amount, message, accepted):
        """
        Using SQL, adds a new exchange into a exchange table
        """
        cursor = self.conn.execute("INSERT INTO exchange (timestamp, sender_id, receiver_id, amount, message, accepted, user_id) VALUES(?,?,?,?,?,?, ?);", (10,sender_id, receiver_id, amount, message, accepted, sender_id))
        self.conn.commit()
        return cursor.lastrowid

    def get_exchange_by_id(self, id):
        """
        Using SQL, get an exchange by its id
        """
        cursor = self.conn.execute("SELECT * FROM exchange where id=?;", (id,))
        for row in cursor:
            return {
                "id" : row[0],
                "timestamp" : row[1],
                "sender_id" : row[2],
                "receiver_id" : row[3],
                "amount" : row[4],
                "message" : row[5],
                "accepted" : row[6]
            }
        return None

    def update_exchange_by_id(self, id, accepted):
        """
        Using SQL, updates an exchange
        """
        self.conn.execute(
            """
            UPDATE exchange
            SET accepted = ?
            WHERE id = ?;
        """,
        (accepted, id)
        )
        self.conn.commit()

# Only <=1 instance of the database driver
# exists within the app at all times
DatabaseDriver = singleton(DatabaseDriver)