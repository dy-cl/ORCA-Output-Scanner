from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

#Select file type
def select_file_type():
    print('Select File Type:')
    print('1. ORCA')
    print('2. N/A')
    print('3. N/A')
    print('4. N/A')

    choice = input('Enter Choice (1 - 4): ')
    return choice

#Select ORCA task
def select_orca_task():
    print('Select Task:')
    print('1. Final Single Point Energy')
    print('2. Geometry Optimization Step Plot')
    print('3. Final Molecular Orbital Energies')

    choice = input('Enter Choice (1 - 3): ')
    return choice

#Get the final single point energy from ORCA file
def get_final_single_point_energy(file_path):
    last_SPE = None

    with open(file_path, 'r') as file:
        for line in file:
            if 'FINAL SINGLE POINT ENERGY' in line:
                last_SPE = line #Update last_SPE for each time it is found so only the last value is kept

    if last_SPE:
        print('Final Single Point Energy: ' + last_SPE)
    else:
        print('Final Single Point Energy: Not Found')

#Get the geometry optimization steps from ORCA file and plot the energies
def plot_geometry_optimization_steps(file_path):
    energies = []

    with open(file_path, 'r') as file:
        for line in file:
            if 'FINAL SINGLE POINT ENERGY' in line:
                energies.append(float(line.split()[-1].strip()))

    plt.plot(range(len(energies)), energies) #Plot Geometry Optimization steps
    plt.xlabel('Step')
    plt.ylabel('Energy / Ha')
    plt.show()

#Get the molecular orbital energies from ORCA file
def get_molecular_orbital_energies(file_path):
    with open(file_path, 'r') as file:
        table_started = False
        table_lines = []

        for line in file:
            line = line.strip()

            if line == 'NO   OCC          E(Eh)            E(eV)': #Table headings to find
                table_started = True
                table_lines = []  #Clear previous table lines when a new table is encountered

            if table_started == True:
                if not line: #Check if line is empty
                    table_started = False  #End of table
                else:
                    table_lines.append(line)

    if table_lines:
        df = pd.DataFrame([line.split() for line in table_lines[1:]], columns= ['Number', 'Occupancy', 'Energy / Ha', 'Energy / eV'])
        df = df.to_string(index = False)
        print(df)
    else:
        print('Orbital energies table not found in the file.')
  


#Main function
def main():
    file_path = '/home/dylan/Python Projects/ORCA File Scanner/benzyne.txt'
    software_choice = select_file_type()
    print('Your Choice is ' + software_choice + '\n')

    if software_choice == '1':
        task_choice = select_orca_task()

        if task_choice == '1':
            get_final_single_point_energy(file_path)
        elif task_choice == '2':
            plot_geometry_optimization_steps(file_path)
        elif task_choice == '3':
            get_molecular_orbital_energies(file_path)


#Run the main function
if __name__ == '__main__':
    main()