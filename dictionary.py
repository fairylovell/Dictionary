import vars, data, states
from security import security

def add(word_en, word_sk):
    vars.dictionary.append([security.encode(vars.password, word_en), security.encode(vars.password, word_sk)])

    for i in range(len(vars.database)):
        if not security.hash_check(vars.database[i][1], vars.email):
            continue
        
        if data.update("dictionaries/" + vars.database[i][1].replace(":", ""), vars.dictionary):
            print(states.OKGREEN + "Added.")
            return

def find(word):
    for y in range(2):
        for i in range(len(vars.dictionary)):
            dec = security.decode(vars.password, vars.dictionary[i][y])

            if not dec == word:
                continue

            print(states.OKGREEN + 'Found.')

            if y == 0:
                print(states.INFO + 'SK: ' + security.decode(vars.password, vars.dictionary[i][1]))
            else:
                print(states.INFO + 'EN: ' + security.decode(vars.password, vars.dictionary[i][0]))

            input(states.INFO + 'Press Enter To Continue...')
            return
    
    print(states.ERROR + word + ' Not Found.')
    input(states.INFO + 'Press Enter To Continue...')

def delete(word):
    for y in range(2):
        for i in range(len(vars.dictionary)):
            dec = security.decode(vars.password, vars.dictionary[i][y])

            if not dec == word:
                continue
            
            vars.dictionary[i][0] = ""
            vars.dictionary[i][1] = ""
                
            if data.update('dictionaries/' + vars.database[i][1].replace(":", ""), vars.dictionary):
                print(states.OKGREEN + 'Deleted.')
                
            return

    print(states.ERROR + word + ' Not Found.')
