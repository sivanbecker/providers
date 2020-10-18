from psycopg2 import OperationalError

def create_db(db, username, pw):
    try:
        db.create_all()
    except OperationalError:
        cmd_create_user = f'CREATE USER {username} WITH PASSWORD {pw}'
        import pudb;pu.db
        db.session.execute(cmd_create_user)
