from datetime import date, datetime
import psycopg2

try:
    conn = psycopg2.connect(dbname='EchoData',
                            user='mynewuser',
                            password='mypassword',
                            host='188.225.42.91',
                            )
except Exception as exept:
    print(f'Can`t establish connection to database. {exept}')

tables_pk = {
    'chats': 'chat_id',
    'keys': 'key_id',
    'tg_action': 'chat_id',
    'bots': 'bot_id',
}


def json_serial(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


def update_chats(chat_id, username=None, balance=None):
    if conn is None:
        return
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
    if conn is None:
        return
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


def update_keys(key_id, base_key=None, secret_key=None, key_name=None, bourse=None):
    if conn is None:
        return
    try:
        with conn.cursor() as curs:
            updates = []
            params = []
            if base_key is not None:
                updates.append("base_key = %s")
                params.append(base_key)

            if secret_key is not None:
                updates.append("secret_key = %s")
                params.append(secret_key)

            if key_name is not None:
                updates.append("key_name = %s")
                params.append(key_name)

            if bourse is not None:
                updates.append("bourse = %s")
                params.append(bourse)

            if not updates:
                print("No fields to update")
                return

            update_query = f"UPDATE keys SET {', '.join(updates)} WHERE key_id = %s"
            params.append(key_id)

            curs.execute(update_query, tuple(params))
            conn.commit()
            print("Record updated successfully")
    except Exception as e:
        print(f"An error occurred while updating the record: {e}")


def update_bots(bot_id, bot_name=None, symbol=None, side=None, reinvestment=None, size=None, status=None):
    if conn is None:
        return
    try:
        with conn.cursor() as curs:
            updates = []
            params = []
            if bot_name is not None:
                updates.append("bot_name = %s")
                params.append(bot_name)

            if symbol is not None:
                updates.append("symbol = %s")
                params.append(symbol)

            if side is not None:
                updates.append("side = %s")
                params.append(side)

            if reinvestment is not None:
                updates.append("reinvestment = %s")
                params.append(reinvestment)

            if size is not None:
                updates.append("size = %s")
                params.append(size)

            if status is not None:
                updates.append("status = %s")
                params.append(status)

            if not updates:
                print("No fields to update")
                return

            update_query = f"UPDATE bots SET {', '.join(updates)} WHERE bot_id = %s"
            params.append(bot_id)

            curs.execute(update_query, tuple(params))
            conn.commit()
            print("Record updated successfully")
    except Exception as e:
        print(f"An error occurred while updating the record: {e}")


def create_chats(chat_id, username, balance=0, is_follow=False):
    if conn is None:
        return
    try:
        with conn.cursor() as curs:
            params = (chat_id, username, balance, is_follow,)
            update_query = f"INSERT INTO chats(chat_id, username, balance, is_follow) VALUES (%s, %s, %s, %s);"

            curs.execute(update_query, params)
            conn.commit()
            print("Record created successfully")
    except Exception as e:
        print(f"An error occurred while updating the record: {e}")


def create_actions(chat_id, action):
    if conn is None:
        return
    try:
        with conn.cursor() as curs:
            params = (chat_id, action,)
            update_query = f"INSERT INTO tg_actions (chat_id, action) VALUES (%s, %s);"

            curs.execute(update_query, params)
            conn.commit()
            print("Record created successfully")
    except Exception as e:
        print(f"An error occurred while updating the record: {e}")


def create_keys(chat_id, base_key=None, secret_key=None, key_name=None, bourse=None):
    if conn is None:
        return
    try:
        with conn.cursor() as curs:
            params = (chat_id, base_key, secret_key, key_name, bourse,)
            update_query = f"INSERT INTO keys (chat_id, base_key, secret_key, key_name, bourse) VALUES "\
                           f"(%s, %s, %s, %s, %s);"

            curs.execute(update_query, params)
            conn.commit()
            print("Record created successfully")
    except Exception as e:
        print(f"An error occurred while updating the record: {e}")


def create_bots(key_id, bot_name=None, symbol=None, side=None, reinvestment=None, size=None, status='inactive'):
    if conn is None:
        return
    try:
        with conn.cursor() as curs:
            params = (key_id, bot_name, symbol, side, reinvestment, size, status, )
            update_query = f"INSERT INTO bots (key_id, bot_name, symbol, side, reinvestment, size, status) VALUES "\
                           f"(%s, %s, %s, %s, %s, %s, %s);"

            curs.execute(update_query, params)
            conn.commit()
            print("Record created successfully")
    except Exception as e:
        print(f"An error occurred while updating the record: {e}")


def delete_record(table_name, pk):
    if conn is None:
        return
    try:
        with conn.cursor() as curs:
            params = (pk,)
            update_query = f"DELETE FROM {table_name} WHERE {tables_pk[table_name]} = %s;"

            curs.execute(update_query, params)
            conn.commit()
            print("Record deleted successfully")
    except Exception as e:
        print(f"An error occurred while deleting the record: {e}")


def create_table():
    if conn is None:
        return
    try:
        # Chats
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

        # tg_actions
        with conn.cursor() as curs:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS tg_actions (
                chat_id SERIAL PRIMARY KEY,
                action VARCHAR(50)
            );
            """
            curs.execute(create_table_query)
            conn.commit()

        # Keys
        with conn.cursor() as curs:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS Keys (
                key_id SERIAL PRIMARY KEY,
                chat_id INTEGER,
                base_key VARCHAR(100),
                secret_key VARCHAR(100),
                key_name VARCHAR(100),
                bourse VARCHAR(100),
                FOREIGN KEY (chat_id) REFERENCES Chats (chat_id)
            );
            """
            curs.execute(create_table_query)
            conn.commit()

        # Bots
        with conn.cursor() as curs:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS Bots (
                bot_id SERIAL PRIMARY KEY,
                key_id INTEGER,
                bot_name VARCHAR(100),
                symbol VARCHAR(20),
                side VARCHAR(10),
                reinvestment INTEGER,
                size INTEGER,
                status VARCHAR(20),
                FOREIGN KEY (key_id) REFERENCES Keys (key_id)
            );
            """
            curs.execute(create_table_query)
            conn.commit()

    except Exception as e:
        print(f"An error occurred while creating the table: {e}")


def make_migrations():
    pass


def read_table(table_name):
    if conn is None:
        return
    try:
        with conn.cursor() as curs:
            curs.execute(f"SELECT * FROM {table_name}")
            column_names = [desc[0] for desc in curs.description]
            all_users = curs.fetchall()

            users_list = [dict(zip(column_names, row)) for row in all_users]
            return users_list
    except Exception as e:
        print(f"An error occurred while reading the table: {e}")
        return None


def get_editable_bots(chat_id):
    if conn is None:
        return
    try:
        with conn.cursor() as curs:
            select_query = """
            SELECT *
            FROM Bots
            JOIN Keys ON Bots.key_id = Keys.key_id
            WHERE Keys.chat_id = %s
            ORDER BY bot_id DESC
            LIMIT 1;
            """
            curs.execute(select_query, (chat_id,))
            column_names = [desc[0] for desc in curs.description]
            bot_ids = curs.fetchall()
            users_list = [dict(zip(column_names, row)) for row in bot_ids]

            return users_list[0]
    except Exception as e:
        print(f"An error occurred while reading the table: {e}")
        return None


def get_editable_keys(chat_id):
    if conn is None:
        return
    try:
        with conn.cursor() as curs:
            select_query = """
            SELECT *
            FROM Keys
            WHERE Keys.chat_id = %s
            ORDER BY key_id DESC
            LIMIT 1;
            """
            curs.execute(select_query, (chat_id,))
            column_names = [desc[0] for desc in curs.description]
            bot_ids = curs.fetchall()

            users_list = [dict(zip(column_names, row)) for row in bot_ids]
            return users_list[0]
    except Exception as e:
        print(f"An error occurred while reading the table: {e}")
        return None


def get_active_bots():
    if conn is None:
        return
    try:
        with conn.cursor() as curs:
            select_query = """
            SELECT bot_id, bot_name, symbol, side, reinvestment, size, status, base_key, secret_key, bourse FROM Bots
            JOIN Keys ON Keys.key_id = Bots.key_id
            WHERE status = 'waiting';
            """
            curs.execute(select_query)
            column_names = [desc[0] for desc in curs.description]
            bots = curs.fetchall()
            users_list = [dict(zip(column_names, row)) for row in bots]
            return users_list
    except Exception as e:
        print(f"An error occurred while reading the table: {e}")
        return None


def get_actions(chat_id):
    if conn is None:
        return
    try:
        with conn.cursor() as curs:
            select_query = """
            SELECT action FROM tg_actions WHERE chat_id = %s
            """
            curs.execute(select_query, (chat_id,))
            action_id = curs.fetchall()
            return action_id[0][0]
    except Exception as e:
        print(f"An error occurred while reading the table: {e}")
        return None


def main():
    create_table()
    # print(get_actions(234223123))
    #for i in range(150):
    #    create_bots(1, bot_name=f'Bot{50+i}', symbol='BTCUSDT', side='Buy', reinvestment=0, size=50, status='waiting')
    # print(get_active_bots())
    #print(get_editable_bots(841051288))
    conn.close()


if __name__ == '__main__':
    main()

