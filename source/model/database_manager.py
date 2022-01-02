import mysql.connector


def connect():
  try:
    connection = mysql.connector.connect(
    host="localhost",
    user="cryptocoin-viewer",
    passwd="pRsxCjiqu}Laq(wF[y46_>v]ugTq1[TjEiUy",
    database="cryptocoin"
    )
    return connection
  except (Exception, mysql.connector.Error) as error:
    return error


def store_user(user, passwd):
  try:
    connection = connect()
    cursor = connection.cursor(buffered=True)
    query = 'insert into users (user, passwd) values (%s, %s)'
    record_to_insert = [user, passwd]
    cursor.execute(query, record_to_insert)
    connection.commit()
    cursor.close()
    connection.close()
    return True
  except (Exception, mysql.connector.Error) as error:
    return error


def find_user(user):
  try:
    connection = connect()
    cursor = connection.cursor()
    query = 'select * from users where user = %s'
    record_to_insert = [user]
    cursor.execute(query, record_to_insert)
    response = cursor.fetchone()
    cursor.close()
    connection.close()
    return (response[1], response[2])
  except (Exception, mysql.connector.Error) as error:
    return error

def delete_user(user, passwd):
  try:
    connection = connect()
    cursor = connection.cursor()
    query = 'delete from users where user = %s and passwd = %s '
    record_to_insert = [user, passwd]
    cursor.execute(query, record_to_insert)
    connection.commit()
    cursor.close()
    connection.close()
    return True
  except (Exception, mysql.connector.Error) as error:
    return error

def get_public_and_private_key_status(user):
  try:
    connection = connect()
    cursor = connection.cursor()
    query = 'select (has_private_and_public_key) from users where user = %s'
    record_to_insert = [user]
    cursor.execute(query, record_to_insert)
    response = cursor.fetchone()
    connection.commit()
    cursor.close()
    connection.close()
    return response
  except (Exception, mysql.connector.Error) as error:
    return error

def store_public_key(user, public_key):
  try:
    connection = connect()
    cursor = connection.cursor()
    query = 'update users set public_key = %s where user = %s'
    record_to_insert = [public_key, user]
    cursor.execute(query, record_to_insert)
    connection.commit()
    cursor.close()
    connection.close()
    return True
  except (Exception, mysql.connector.Error) as error:
    return error


def change_public_and_private_key_status(user, public_key):
  try:
    connection = connect()
    cursor = connection.cursor()
    if get_public_and_private_key_status(user) == (0,):
      query = 'update users set has_private_and_public_key = 1 where user = %s and public_key = %s'
      record_to_insert = [user, public_key]
      cursor.execute(query, record_to_insert)
      connection.commit()
      cursor.close()
      connection.close()
      return True, "The user now have a public and private key"
    else:
      return False, "The user already have a public and private key"
  except (Exception, mysql.connector.Error) as error:
    return error