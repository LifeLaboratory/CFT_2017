import sys
import os
directory_user_cabinet = os.getcwd()
sys.path.insert(0, directory_user_cabinet)
from connect_db import connect_db

conn, c = connect_db()
