import colorama, sys, registration, login, vars, data, dictionary, states, os
from security import security

colorama.init()
data.read('database', vars.database)
os.makedirs("dictionaries", exist_ok = True)

while True:
    if vars.loggedin:
        choice = input(states.INFO +\
        '┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n\
      ┃ Welcome ' + vars.name + (25-len(vars.name))*' ' + '┃\n\
      ┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫\n\
      ┃1. Add New Word To Dictionary     ┃\n\
      ┃2. Find A Word In Dictionary      ┃\n\
      ┃3. Delete A Word From Dictionary  ┃\n\
      ┃                                  ┃\n\
      ┃4. Change Email Address           ┃\n\
      ┃5. Change Password                ┃\n\
      ┃6. Logout                         ┃\n\
      ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n\
      Enter Your Choice: ')
        if choice == '1':
            dictionary.add(input(states.INFO + 'EN: '), input(states.INFO + 'SK: '))
        elif choice == '2':
            dictionary.find(input(states.INFO + 'Word: '))
        elif choice == '3':
            dictionary.delete(input(states.INFO + 'Word: '))
        elif choice == '4':
            security.change_email()
        elif choice == '5':
            security.change_password()
        elif choice == '6':
            vars.loggedin = False
        else:
            print(states.ERROR + 'Invalid Option. Try Again.')

    else:
        choice = input(states.INFO +\
         '┏━━━━━━━━━━━━━━┓\n\
      ┃  Dictionary  ┃\n\
      ┣━━━━━━━━━━━━━━┫\n\
      ┃1. Login      ┃\n\
      ┃2. Register   ┃\n\
      ┃              ┃\n\
      ┃3. Exit       ┃\n\
      ┗━━━━━━━━━━━━━━┛\n\
      Enter Your Choice: ')

        if choice == '1':
            if login.login() == False:
                sys.exit()
        elif choice == '2':
            registration.registration()
        elif choice == '3':
            print(states.INFO + 'Exiting Program...')
            sys.exit(0)
        else:
            print(states.ERROR + 'Invalid Option. Try Again.')
