import sqlalchemy

def get_all_usr(conn)->list:
    return conn.execute(sqlalchemy.text("""SELECT username, attr_level FROM users""")).fetchall()

def change_attr_lvl(username, attr_lvl, conn):

    attr_lvl = int(attr_lvl)
    if attr_lvl == 0:
        conn.execute(sqlalchemy.text(f"""DELETE FROM users WHERE username = '{username}'"""))

    conn.execute(sqlalchemy.text(f"""UPDATE users SET attr_level = {attr_lvl} WHERE username = '{username}'"""))
    return None