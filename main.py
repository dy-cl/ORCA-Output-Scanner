from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import os 
import re

class Menu:
    #Select file type
    @staticmethod
    def select_file_type():
        print('Select File Type:')
        print('1. ORCA')
        print('2. N/A')
        print('3. N/A')
        print('4. N/A')
        print('\n')

        choice = input('Enter Choice (1 - 4): ')
        print('\n')
        return choice

    #Select ORCA task
    @staticmethod
    def select_orca_task():
        print('Select Task:')
        print('1. Final Single Point Energy')
        print('2. Geometry Optimization Step Plot')
        print('3. Final Molecular Orbital Energies')
        print('4. Loewdin Atomic Charges')
        print('5. Vibrational Frequencies')
        print('\n')

        choice = input('Enter Choice (1 - 5): ')
        print('\n')
        return choice


class ORCAFileProcessor:
    #Get the final single point energy from ORCA file
    @staticmethod
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
    @staticmethod
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
    @staticmethod
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


    #Get Lowedin Atomic Charges
    @staticmethod
    def get_loewdin_charges(file_path):
        with open(file_path, 'r') as file:
            file_contents = file.read()

            #Find the last occurrence of the table
            last_table_start = file_contents.rfind('LOEWDIN ATOMIC CHARGES')
            last_table_end = file_contents.find('-------------------------------', last_table_start)

            if last_table_start == -1 or last_table_end == -1:
                print('No "Loewdin Charges" table found.')
                return

            #Extract the table contents
            table_contents = file_contents[last_table_start:last_table_end]

            #Process the table
            table_lines = table_contents.strip().split('\n')[2:]  # Remove header and footer lines

            table_data = [line.split(':') for line in table_lines]
            df = pd.DataFrame(table_data, columns=['Atom', 'Loewdin Charge'])
            print(df.to_string(index=False))

    #Get IR Spectrum (Vibrational Frequencies) and plot
    @staticmethod
    def get_vibrational_frequencies(file_path):
        with open(file_path, 'r') as file:
            file_contents = file.read()

            #Find the start of the table
            table_start = file_contents.find('cm**-1   L/(mol*cm) km/mol    a.u.')

            if table_start == -1:
                print('Table not found.')
                return

            #Find the end of the table
            table_end = file_contents.find('* The epsilon (eps) is given for a Dirac delta lineshape.', table_start)

            if table_end == -1:
                print('End of table not found.')
                return

            #Extract table contents and process
            table_contents = file_contents[table_start:table_end]
            table_lines = table_contents.strip().split('\n')[2:]
            data = [item for item in table_lines if item]
            data = [string.strip() for string in data]

            extracted_data = []

            #Sort values into columns
            for item in data:
                values = [
                    str(item[0:5]),
                    float(item[6:14]),
                    float(item[15:26]),
                    float(item[27:32]),
                    float(item[33:42]),
                    float(item[45:54]),
                    float(item[55:64]),
                    float(item[65:73])
                ]

                extracted_data.append(values)

            df = pd.DataFrame(extracted_data, columns = ["Mode", "Frequency", "eps", "Intensity", "T**2", "TX", "TY", "TZ"])
            print(df)

            plt.plot( df['Frequency'], df['Intensity'])
            plt.gca().invert_yaxis()
            plt.show()
        


#Main function
def main():

    ### CHANGE FILE HERE ###
    file_path = '/home/dylan/Python Projects/ORCA File Scanner/trans13bd.txt'
    menu = Menu()
    software_choice = menu.select_file_type() 

    if software_choice == '1':
        task_choice = menu.select_orca_task()

        if task_choice == '1':
            ORCAFileProcessor.get_final_single_point_energy(file_path)
        elif task_choice == '2':
            ORCAFileProcessor.plot_geometry_optimization_steps(file_path)
        elif task_choice == '3':
            ORCAFileProcessor.get_molecular_orbital_energies(file_path)
        elif task_choice == '4':
            ORCAFileProcessor.get_loewdin_charges(file_path)
        elif task_choice == '5':
            ORCAFileProcessor.get_vibrational_frequencies(file_path)

#Run main
if __name__ == '__main__':
    main()