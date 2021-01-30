import states, vars

def read(file, array):
    array.clear()
    try:
        with open(file, 'r') as f:
            data = f.readlines()
            for i in data:
                array.append(i.split())

    except FileNotFoundError:
        with open(file, 'w') as f:
            if array == vars.database:
                print(states.ERROR + 'Database Not Found.')
                print(states.INFO + 'Creating Database...')
            elif array == vars.dictionary:
                print(states.ERROR + 'Dictionary Not Found.')
                print(states.INFO + 'Creating Dictionary...')

def update(file, array):
    try:
        with open(file, 'w') as f:
            data = []
            for i in range(len(array)):
                if array == vars.dictionary and vars.dictionary[i][0] == "":
                    continue
                data.append(" ".join(array[i]))
            f.truncate()
            f.write("\n".join(data))
        return True
    except Exception as e:
        print(states.ERROR + str(e))
        return False
