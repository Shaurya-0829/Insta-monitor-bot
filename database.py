import sqlite3

DATABASE = "monitor.db"


def get_connection():
    return sqlite3.connect(DATABASE)


def init_db():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS monitors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            started_at TEXT NOT NULL,
            mode TEXT NOT NULL,
            active INTEGER NOT NULL DEFAULT 1
        )
    """)

    connection.commit()
    connection.close()


def add_monitor(
    username: str,
    started_at: str,
    mode: str,
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO monitors (
            username,
            started_at,
            mode,
            active
        )
        VALUES (?, ?, ?, 1)
        """,
        (
            username,
            started_at,
            mode,
        )
    )

    connection.commit()
    connection.close()


def get_monitor(username: str):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            username,
            started_at,
            mode,
            active
        FROM monitors
        WHERE username = ?
          AND active = 1
        """,
        (username,)
    )

    row = cursor.fetchone()

    connection.close()

    return row


def stop_monitor(username: str):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE monitors
        SET active = 0
        WHERE username = ?
        """,
        (username,)
    )

    connection.commit()
    connection.close()

def get_active_monitors():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            username,
            started_at,
            mode,
            active
        FROM monitors
        WHERE active = 1
        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()

    connection.close()

    return rows

def stop_all_monitors():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE monitors
        SET active = 0
        WHERE active = 1
        """
    )

    cancelled_count = cursor.rowcount

    connection.commit()
    connection.close()

    return cancelled_count

def get_monitor_stats():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM monitors
        WHERE active = 1
        """
    )

    total = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM monitors
        WHERE active = 1
          AND mode = 'active'
        """
    )

    active_monitors = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM monitors
        WHERE active = 1
          AND mode = 'unavailable'
        """
    )

    unavailable_monitors = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM monitors
        WHERE active = 0
        """
    )

    completed = cursor.fetchone()[0]

    connection.close()

    return (
        total,
        active_monitors,
        unavailable_monitors,
        completed,
    )



DATABASE = "monitor.db"


def get_connection():
    return sqlite3.connect(DATABASE)


# =========================================================
# ADMIN TABLE
# =========================================================

def init_admins():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            user_id INTEGER PRIMARY KEY
        )
    """)

    # Always make the original ADMIN_ID an admin
    from config import ADMIN_ID

    cursor.execute(
        """
        INSERT OR IGNORE INTO admins (user_id)
        VALUES (?)
        """,
        (ADMIN_ID,)
    )

    connection.commit()
    connection.close()


def is_admin(user_id: int) -> bool:

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT 1
        FROM admins
        WHERE user_id = ?
        """,
        (user_id,)
    )

    result = cursor.fetchone()

    connection.close()

    return result is not None


def add_admin(user_id: int) -> bool:

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT OR IGNORE INTO admins (user_id)
        VALUES (?)
        """,
        (user_id,)
    )

    added = cursor.rowcount > 0

    connection.commit()
    connection.close()

    return added


def remove_admin(user_id: int) -> bool:

    from config import ADMIN_ID

    # Never allow the original owner to be removed
    if user_id == ADMIN_ID:
        return False

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM admins
        WHERE user_id = ?
        """,
        (user_id,)
    )

    removed = cursor.rowcount > 0

    connection.commit()
    connection.close()

    return removed


def get_admins():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT user_id
        FROM admins
        ORDER BY user_id
        """
    )

    rows = cursor.fetchall()

    connection.close()

    return [row[0] for row in rows]