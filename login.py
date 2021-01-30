import vars, states, data, getpass
from security import security

def login():
    vars.email = input(states.INFO + 'Email Address: ')

    if vars.email == '':
        print(states.ERROR + 'Invalid Email Address.')
        return True
    
    if vars.email.find('@') == -1:
        print(states.ERROR + 'Invalid Email Address.')
        return True

    vars.password = getpass.getpass(states.INFO + 'Password: ')

    for i in range(len(vars.database)):
        if not security.hash_check(vars.database[i][0], vars.password):
            continue
        
        if security.hash_check(vars.database[i][1], vars.email):
            vars.name = security.decode(vars.password, vars.database[i][2])
            vars.counter = 0
            data.read('dictionaries/' + vars.database[i][1].replace(":", ""), vars.dictionary)
            vars.loggedin = True
            print(states.OKGREEN + 'Logged In.')
            return True

    vars.counter += 1
    print(states.ERROR + 'Wrong Email Or Password')

    if vars.counter == 3:
        print(states.ERROR + 'Too Many Unsuccessful Login Attempts.')
        print(states.INFO + 'Exiting Program...')
        return False
