def menu():
    print('Select File Type: ')
    print('1. ORCA')
    print('2. N/A')
    print('3. N/A')
    print('4. N/A')
  
    choice = input('Enter Choice (1-4): ')
    return choice

user_choice = menu()
print('Your Choice is ' + user_choice)
