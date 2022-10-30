import click
from flask import current_app, g
from flask.cli import with_appcontext
import psycopg2
from psycopg2.extras import DictCursor
import os
from werkzeug.security import generate_password_hash

def get_db():
    if 'conn' not in g:
        g.conn = psycopg2.connect(
            database=os.environ.get('DATABASE'),
            user=os.environ.get('DATABASE_USER'),
            password=os.environ.get('DATABASE_PASSWORD'),
            host=os.environ.get('DATABASE_HOST'),
            port=os.environ.get('DATABASE_PORT')
        )
        """g.conn = psycopg2.connect(
            database='flaskr',
            user='inoueyuya',
            #ppassword='inoue0811',
            #host='127.0.0.1',
            #port='5000'
        )"""
        g.cur = g.conn.cursor(cursor_factory=DictCursor)
    return g.cur

def close_db(e=None):
    db_conn = g.pop('conn', None)
    db_cur = g.pop('cur', None)
    if db_conn is not None:
        db_conn.close()
    if db_cur is not None:
        db_cur.close()

def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.execute(f.read().decode('utf8'))
    g.conn.commit()

def checkColumns(cur, cmd):
    try:
        cur.execute(cmd)
        print(cmd)
        return True
    except:
        return None

@click.command('delete-columns')
@with_appcontext
def delete_columns_command():
    print("*** START ***")
    counter = 0
    cur = get_db()
    print("PHASE posts...")
    cmd_select = "SELECT gender FROM posts"
    if checkColumns(cur, cmd_select):
        counter += 1
    cmd_drop = "ALTER TABLE posts DROP COLUMN gender"
    if counter > 0:
        cur.execute(cmd_drop)
        g.conn.commit()
    else:
        print("Element: 0")
    close_db()
    print("--- FIN ---")
    print()

    cur = get_db()
    nums = []
    counter = 0
    print("PHASE users...")

    cmds_select = ["SELECT i_o FROM users",
                   "SELECT username FROM users",
                   "SELECT gender FROM users",
                   "SELECT age FROM users",
                   "SELECT password FROM users"
                  ]
    #Check
    for cmd in cmds_select:
        print('select: cmd')
        print(cmd)
        if checkColumns(cur, cmd):
            nums.append(counter)
        counter += 1

    cmds_drop = ["ALTER TABLE users DROP COLUMN i_o",
                 "ALTER TABLE users DROP COLUMN username",
                 "ALTER TABLE users DROP COLUMN gender",
                 "ALTER TABLE users DROP COLUMN age",
                 "ALTER TABLE users DROP COLUMN password"
                ]
    if len(nums) > 0:
        for num in nums:
            cur.execute(cmds_drop[num])
        g.conn.commit()
    else:
        print("Element: 0")
    close_db()
    print("--- FIN ---")
    print()
    print("COMPLTE DELTE COLUMNS.")


@click.command('setting-data')
@with_appcontext
def setting_data_command():
    print('*** START ***')
    file = open(file='text_data/tweet.txt', mode='r', encoding='utf_8')
    dic = {}
    i=0
    for f in file:
        dic['t_v{}'.format(i)] = [f.replace('\n', '')]
        i+=1

    file.close()
    file = open(file='text_data/tweet_kana.txt', mode='r', encoding='utf_8')
    i = 0
    for f in file:
        dic['t_v{}'.format(i)].append(f.replace('\n', ''))
        dic['t_v{}'.format(i)].append(0)
        i+=1
    file.close()
    cur = get_db()
    for k, v in dic.items():
        cur.execute(
            'INSERT INTO tweets (file_id, file_title, kana, num, created) VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)',
            (k, v[0], v[1], v[2])
        )
    print('Tweet commit.')
    g.conn.commit()
    close_db()
    file = open(file='text_data/ita.txt', mode='r', encoding='utf_8')
    dic = {}
    i=0
    for f in file:
        dic['i_v{}'.format(i)] = [f.replace('\n', '')]
        i+=1

    file.close()
    file = open(file='text_data/ita_kana.txt', mode='r', encoding='utf_8')
    i = 0
    for f in file:
        dic['i_v{}'.format(i)].append(f.replace('\n', ''))
        dic['i_v{}'.format(i)].append(0)
        i+=1
    file.close()
    cur = get_db()
    for k, v in dic.items():
        cur.execute(
            'INSERT INTO itas (file_id, file_title, kana, num, created) VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)',
            (k, v[0], v[1], v[2])
        )
    print('ITA commit.')
    g.conn.commit()
    close_db()

    cur = get_db()
    cur.execute("INSERT INTO admins (id, password) VALUES (%s, %s)",
        (os.environ.get('ADMIN_ID'), generate_password_hash(os.environ.get('ADMIN_PASSWORD')))
    )
    print('admins commit.')
    g.conn.commit()
    close_db()
    click.echo('Setting data complete.')


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(setting_data_command)
    app.cli.add_command(delete_columns_command)
