from database_manager import store_user, find_user, connect
import getpass


def prompt_user():
  print()
  user = input("Provide your username: ").replace(" ", "")
  print()
  passwd = getpass.getpass("Provide your password: ").replace(" ", "")

  return user, passwd

def main():
  print("Do you have an account? [y/n]")

  while True:
    response = input()
    response = response.replace(" ", "").lower()[0]
    if response == "y" or response == "n":
      break
    else:
      print()
      print("Invalid response! Answer only \"y\" or \"n\"")

  while True:
    user, passwd = prompt_user()

    if response == "y":
      result = find_user(user, passwd)
      if result == None:
        print("Username or password wrong ")
      elif result[1] == user and result[2] == passwd:
        print("Sucessfully logged! ")
        break
    if response == "n":
      result = store_user(user, passwd)
      if result == None:
        print("Your username and password was successfully stored!")
      break

    return True

if __name__ == '__main__':
  main()