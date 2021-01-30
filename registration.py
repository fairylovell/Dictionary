import vars, data, states, getpass
from security import security

def registration():

    vars.name = input(states.INFO + 'Name: ')        

    if len(vars.name) > 15:
        print(states.ERROR + 'Invalid Name. (Max 15 Characters)')
        return

    vars.email = input(states.INFO + 'Email Address: ')

    if vars.email == '':
        print(states.ERROR + 'Invalid Email Address.')
        return
    
    if vars.email.find('@') == -1:
        print(states.ERROR + 'Invalid Email Address.')
        return

    for i in range(len(vars.database)):
        if security.hash_check(vars.database[i][1], vars.email):
            print(states.ERROR + 'Account With This Email Address Already Exists.')
            return

    vars.password = getpass.getpass(states.INFO + 'New Password: ')
        
    if vars.password == '':
       print(states.ERROR + 'Invalid Password.')
       return

    if not vars.password == getpass.getpass(states.INFO + 'Retype New Password: '):
       print(states.ERROR + 'Passwords Don\'t Match')
       return

    choice = input(states.INFO + 'Do You Want To Continue? (Y/N): ')

    if choice == 'N' or choice == 'n':
       print(states.ERROR + 'Registration Cancelled.')
       return

    if not (choice == 'Y' or choice == 'y'):
       print(states.ERROR + 'Invalid option.')
       return

    print(states.OKGREEN + 'Verification Process Initiated.')

    if vars.skip == False:
        sec = security()

        if not sec.sendmail(vars.name, vars.email):
            print(states.ERROR + 'Verification Failed. Try It Again Later.')

        if not sec.verification():
            print(states.ERROR + 'Verification unsuccessful.')
            return

    print(states.OKGREEN + 'Account Created.')
    print(states.INFO + 'Saving Data...')

    email_hash = security.hash_it(vars.email)

    vars.database.append([\
        (security.hash_it(vars.password)),\
        (email_hash),\
        (security.encode(vars.password, vars.name))])
            
    with open('dictionaries/' + email_hash.replace(":", ""), 'w') as f:
        pass

    if data.update('database', vars.database):
        print(states.OKGREEN + 'Data Saved. You Can Log In.')
