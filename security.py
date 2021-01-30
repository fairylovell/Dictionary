import vars, base64, uuid, hashlib, vars, smtplib, secrets, data, states, os, email_template, getpass

class security:
    code = 0
    
    def encode(key, string): # https://stackoverflow.com/a/2490718/9415502
        encoded_chars = []

        for i in range(len(string)):
            encoded_c = chr(ord(string[i]) + ord(key[i % len(key)]))
            encoded_chars.append(encoded_c)
        
        return base64.b64encode(bytes("".join(encoded_chars), 'UTF-8')).decode()

    def decode(key, string):
        encoded_chars = []
        dec = base64.b64decode(string.encode()).decode()
        
        for i in range(len(dec)):
            encoded_c = chr(ord(dec[i]) - ord(key[i % len(key)]))
            encoded_chars.append(encoded_c)
        
        return "".join(encoded_chars)

    def hash_it(it): # https://www.pythoncentral.io/hashing-strings-with-python/
        salt = uuid.uuid4().hex
        return hashlib.sha256(salt.encode() + it.encode()).hexdigest() + ':' + salt
    
    def hash_check(hashed_it, it):
        t_hash, salt = hashed_it.split(':')
        return t_hash == hashlib.sha256(salt.encode() + it.encode()).hexdigest()

    def verification(self):
        for i in range(4):
            if input() == str(self.code):
                return True
                
            choice = states.colinput(states.ERROR + 'You Entered Wrong Code. Do You Want To Try It Again? (Y/N): ')                
                
            if choice == 'Y' or choice == 'y':
                print(states.INFO + 'Write Your Code: ', end='')
                continue
                
            elif choice == 'N' or choice == 'n':
                print(states.ERROR + 'Verification Process Cancelled.')
                return False
            
            else:
                print(states.ERROR + 'Invalid Option.')
                return False

        print(states.ERROR + 'Maximum Number Of Allowed Attempts Reached.')
        return False

    def sendmail(name, recipient):
        to = [recipient]
        self.code = 1000 + secrets.randbelow(9000)
        subject = 'Verify Email Address For Dictionary'

        body = email_template.mail_structure.format(name, self.code)

        email_text = """\
From: %s
To: %s
Content-type: text/html
Subject: %s

%s
""" % (vars.user_c, ", ".join(to), subject, body)

        try:
            print(states.INFO + "Sending Email...")

            with smtplib.SMTP_SSL(vars.smtp_c, vars.port_c) as server:
                server.ehlo()
                server.login(vars.user_c, vars.password_c)
                server.sendmail(vars.user_c, to, email_text)

            print(states.OKGREEN + 'Sent. Check Your Inbox.')
            print(states.INFO + 'Code: ', end='')
            return True

        except Exception as e:
            print(states.ERROR + str(e))
            return False

    def change_email(self):
        print(states.OKGREEN + 'Verification Process Initiated.')
        sec = security()

        if not sec.sendmail(vars.name, vars.email):
            print(states.ERROR + 'Verification Failed. Try It Again Later.')
            return

        if not sec.verification():
            print(states.ERROR + 'Verification Failed. Try It Again Later.')
            return
        
        print(states.OKGREEN + 'Identity Verified.')
       
        for i in range(len(vars.database)):
            if not security.hash_check(vars.database[i][1], vars.email):
                continue

            vars.email = input(states.INFO + 'New Email Address: ')
                    
            if vars.email == '':
                print(states.ERROR + 'Invalid Email Address.')
                return

            if vars.email.find('@') == -1:
                print(states.ERROR + 'Invalid Email Address.')
                return

            if security.hash_check(vars.database[i][1], vars.email):
                print(states.ERROR + 'Invalid Email Address.')
                return

            sec.sendmail(vars.name, vars.email)
            
            if not sec.verification():
                return
                        
            print(states.OKGREEN + 'Email Address changed.')
            print(states.INFO + 'Saving Data...')
                            
            new_email_hash =  security.hash_it(vars.email)
            os.rename('dictionaries/' + vars.database[i][1].replace(":", ""), 'dictionaries/' + new_email_hash.replace(":", ""))
            vars.database[i][1] = new_email_hash

            if not data.update('database', vars.database):
                print(states.INFO + 'Cannot Change Email Address Right Now.')
                return


    def change_password(self):
        print(states.OKGREEN + 'Verification Process Initiated.')
        sec = security()
        
        if not sec.sendmail(vars.name, vars.email):
            print(states.INFO + 'Cannot Change Your Password Right Now.')
            return
        
        if not sec.verification():
            print(states.ERROR + 'Verification Failed. Try It Again Later.')
            return
                
        print(states.OKGREEN + 'Identity Verified.')

        for i in range(len(vars.database)):
            if not security.hash_check(vars.database[i][1], vars.email):
                continue
            
            temp = vars.password                            
            vars.password = getpass.getpass(states.INFO + 'New Password: ')
            
            if not vars.password == getpass.getpass(states.INFO + 'Retype New Password: '):
                print(states.ERROR + 'Passwords Don\'t Match')
                return

            print(states.INFO + 'Saving Data...')

            for y in range(len(vars.dictionary)):
                vars.dictionary[y][0] = security.encode(vars.password, security.decode(temp, vars.dictionary[y][0]))
                vars.dictionary[y][1] = security.encode(vars.password, security.decode(temp, vars.dictionary[y][1]))
                            
            vars.database[i][0] = security.hash_it(vars.password)
            vars.database[i][2] = security.encode(vars.password, vars.name)

            if data.update('database', vars.database) & data.update('dictionaries/' + vars.database[i][1].replace(":", ""), vars.dictionary):
                print(states.OKGREEN + 'Password Changed.')
                return
            
            print(states.ERROR + 'Cannot Change Password Right Now.')
            return
                    