#_______ENTER OWN FILE PATH HERE_____________
file_path = '/home/dylan/Python Projects/ORCA File Scanner/water.txt'

#Select file type
def menu():
    print('Select File Type: ')
    print('1. ORCA')
    print('2. N/A')
    print('3. N/A')
    print('4. N/A')
  
    choice = input('Enter Choice (1 - 4): ')
    return choice

#Run menu and check choice is returned correctly
software_choice = menu()
print('Your Choice is ' + software_choice + '\n')

#Select task in ORCA
def orca_menu():
    print('Select Task: ')
    print('1. Final Single Point Energy: ')

    choice = input ('Enter Choice (1 - 1): ')
    return choice


#ORCA Files
if software_choice == '1':

    task_choice = orca_menu()
    
    #Final Single Point Energues
    if task_choice == '1':
        found = False
        with open(file_path, 'r') as file:
            for line in file:
                if 'FINAL SINGLE POINT ENERGY' in line:
                    print(line)
                    found = True
                    break
        if not found:
            print('Final Single Point Energy: Not Found')

