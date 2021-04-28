#!/usr/bin/env python3

import pymysql
from pymysql import connections
from aws_config import *

def rds_connect():
    #we create a Connection object that represents a socket with MySQL server
    conn = connections.Connection(
        host = custom_host,
        port = 3306,
        user = custom_user,
        password = custom_pass,
        db = custom_db
    )
    return(conn) 
     
       