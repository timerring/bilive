import sqlite3
import os

# DATA_BASE_FILE ='./data.db'
DATA_BASE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data.db')

def connect():
    db = sqlite3.connect(DATA_BASE_FILE)
    return db

def create_table():
    try:
        db = connect()
        cursor = db.cursor()
        sql = [
            "create table upload_queue (id integer primary key autoincrement, video_path text, config_path text, locked integer default 0);",
            "create unique index idx_video_path on upload_queue(video_path);",
        ]
        for s in sql:
            cursor.execute(s)
        db.commit()
        db.close()
        return True
    except:
        print("Create table failed.")
        return False
    
def get_single_upload_queue():
    db = connect()
    cursor = db.cursor()
    cursor.execute("select video_path, config_path from upload_queue where locked = 0 limit 1;")
    row = cursor.fetchone()
    result = {'video_path': row[0], 'config_path': row[1]} if row else None
    db.close()
    return result

def insert_upload_queue(video_path: str, config_path: str):
    try:
        db = connect()
        cursor = db.cursor()
        cursor.execute("insert into upload_queue (video_path, config_path) values (?, ?);", (video_path, config_path))
        db.commit()
        db.close()
        return True
    except sqlite3.IntegrityError:
        print("Insert Upload Queue failed, the video path already exists.")
        return False
    
def delete_upload_queue(video_path: str):
    try:
        db = connect()
        cursor = db.cursor()
        cursor.execute("delete from upload_queue where video_path = ?;", (video_path,))
        db.commit()
        db.close()
        return True
    except:
        print("Delete Upload Queue failed.")
        return False

def update_upload_queue_lock(video_path: str, locked: int):
    try:
        db = connect()
        cursor = db.cursor()
        cursor.execute("update upload_queue set locked = ? where video_path = ?;", (locked, video_path))
        db.commit()
        db.close()
        return True
    except:
        print("Update Upload Queue failed.")
        return False
    
    
    
if __name__ == "__main__":
    # Create Table
    create_table()
    # Insert Test Data
    insert_upload_queue('test.mp4', 'config.yaml')
    # Insert again to check the unique index
    print(insert_upload_queue('test.mp4', 'config.yaml'))
    # Get the single upload queue, shold be {'video_path': 'test.mp4', 'config_path': 'config.yaml'}
    print(get_single_upload_queue())
    # Delete the upload queue
    delete_upload_queue('test.mp4')
    # Get the single upload queue after delete, should be None
    print(get_single_upload_queue())