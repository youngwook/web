from datetime import datetime
import time
from sqlite3 import dbapi2 as sqlite3


#configuration
DATABASE = 'test.db'

def format_datetime(date):
    return datetime.utcfromtimestamp(date).strftime('%Y-%m-%d @ %H:%M')

def connect_db():
    """Return a new connection to the database."""
    return sqlite3.connect(DATABASE)

def insertuser(name, pwd):
    con = connect_db()
    con.execute('''insert into user (username, pwd) values (?,?)''', (name,pwd))
    con.commit()
    con.close()

def insertblog(title, content, u_id):
    con = connect_db()
    con.execute('''insert into blog (title, content, u_id, time) values (?,?,?,?)''', (title, content, u_id, time.time()))
    con.commit()
    con.close()

def insertword(content, who, whom):
    con = connect_db()
    con.execute('''insert into word (content, who, whom, time) values (?,?,?,?)''', (content, who, whom, time.time()))
    con.commit()
    con.close()
def get():
    con = connect_db()
    messages = query_db(con, '''select blog.*, user.* from blog, user
    where blog.u_id = user.u_id order by blog.time desc limit ?''', [2])
    for message in messages:
        print(message['title'])
        print(message['username'])
        print(format_datetime(message['time']))
        print(message['content'])

    con.close()

def query_db(con, query, args=(), one=False):
    '''query the database and returns a list of dictionaries'''

    cur = con.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]

    return (rv[0] if rv else None) if one else rv

def choose():
    while(True):
        print("choose")
        print("1 user")
        print("2 blog")
        print("3 word")
        a = input("your decision")
        if a == 1:
            print("insert username and pwd")
            name = raw_input("username:")
            pwd = raw_input("passworld:")
            insertuser(name, pwd)
        elif a == 2:
            print("insert title content uid")
            title = raw_input("title:")
            content = raw_input("content:")
            uid = raw_input("uid:")
            insertblog(title, content, int(uid))
        elif a == 3:
            print("insert content, who, whom")
            content = raw_input("content:")
            who = raw_input("who:")
            whom = raw_input("whom:")
            insertword(content, int(who), int(whom))
        elif a == 5:
            get()
        elif a == 4:
            break
        else:
            pass



if __name__ == "__main__":
    choose()
    print("your wellcome!")