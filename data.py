import json
from datetime import date, datetime
import psycopg2

try:
    conn = psycopg2.connect(dbname='EchoData',
                            user='postgres',
                            password='123',
                            host='localhost',
                            )
except:
    print('Can`t establish connection to database')


def json_serial(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


def update_chats(chat_id, username=None, balance=None):
    if conn is not None:
        try:
            with conn.cursor() as curs:
                updates = []
                params = []
                if username is not None:
                    updates.append("username = %s")
                    params.append(username)
                if balance is not None:
                    updates.append("balance = %s")
                    params.append(balance)

                if not updates:
                    print("No fields to update")
                    return

                update_query = f"UPDATE Chats SET {', '.join(updates)} WHERE chat_id = %s"
                params.append(chat_id)

                curs.execute(update_query, tuple(params))
                conn.commit()
                print("Record updated successfully")
        except Exception as e:
            print(f"An error occurred while updating the record: {e}")


def update_actions(chat_id, action=None):
    if conn is not None:
        try:
            with conn.cursor() as curs:
                updates = []
                params = []
                if action is not None:
                    updates.append("action = %s")
                    params.append(action)

                if not updates:
                    print("No fields to update")
                    return

                update_query = f"UPDATE tg_actions SET {', '.join(updates)} WHERE chat_id = %s"
                params.append(chat_id)

                curs.execute(update_query, tuple(params))
                conn.commit()
                print("Record updated successfully")
        except Exception as e:
            print(f"An error occurred while updating the record: {e}")


def create_actions(chat_id, action):
    if conn is not None:
        try:
            with conn.cursor() as curs:
                params = (chat_id, action,)
                update_query = f"INSERT INTO tg_actions (chat_id, action) VALUES (%s, %s);"

                curs.execute(update_query, params)
                conn.commit()
                print("Record updated successfully")
        except Exception as e:
            print(f"An error occurred while updating the record: {e}")


def create_chats(chat_id, username, balance, is_follow=False):
    if conn is not None:
        try:
            with conn.cursor() as curs:
                params = (chat_id, username, balance, is_follow,)
                update_query = f"INSERT INTO chats(chat_id, username, balance, is_follow) VALUES (%s, %s, %s, %s);"

                curs.execute(update_query, params)
                conn.commit()
                print("Record updated successfully")
        except Exception as e:
            print(f"An error occurred while updating the record: {e}")


def create_table():
    if conn is not None:
        try:
            with conn.cursor() as curs:
                create_table_query = """
                CREATE TABLE IF NOT EXISTS Chats (
                    chat_id SERIAL PRIMARY KEY,
                    username VARCHAR(50),
                    balance INT,
                    is_follow BOOLEAN DEFAULT FALSE
                );
                """
                curs.execute(create_table_query)
                conn.commit()

            with conn.cursor() as curs:
                create_table_query = """
                CREATE TABLE IF NOT EXISTS tg_actions (
                    chat_id SERIAL PRIMARY KEY,
                    action VARCHAR(50)
                );
                """
                curs.execute(create_table_query)
                conn.commit()
        except Exception as e:
            print(f"An error occurred while creating the table: {e}")


def make_migrations():
    if conn is not None:
        try:
            with conn.cursor() as curs:
                curs.execute("""
                    SELECT column_name
                    FROM information_schema.columns
                    WHERE table_name='chats' AND column_name='is_follow';
                """)

                if not curs.fetchone():
                    add_column_query = """
                    ALTER TABLE Chats
                    ADD COLUMN is_follow BOOLEAN DEFAULT FALSE;
                    """
                    curs.execute(add_column_query)
                    conn.commit()
        except Exception as e:
            print(f"An error occurred while creating the table: {e}")


def read_table(table_name):
    if conn is not None:
        try:
            with conn.cursor() as curs:
                curs.execute(f"SELECT * FROM {table_name}")
                column_names = [desc[0] for desc in curs.description]
                all_users = curs.fetchall()

                users_list = [dict(zip(column_names, row)) for row in all_users]
                users_json = json.dumps(users_list, default=json_serial, indent=4)
                return users_json
        except Exception as e:
            print(f"An error occurred while reading the table: {e}")
            return None


def main():
    create_table()
    make_migrations()
    # print(read_table('chats'))
    create_chats(234223123, 'bylygeme', 23123)
    conn.close()


if __name__ == '__main__':
    main()
