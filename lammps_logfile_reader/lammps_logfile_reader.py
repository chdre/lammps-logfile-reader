import numpy as np
import re
from pathlib import Path


class ReadLog:
    """Minimalistic program for reading log files created by LAMMPS simulations.
    The content of the logfile is stored in a dictionary. Allowed for easy
    extraction of variables.

    :param inputFile: Full path to logfile
    :type inputFile: str or pathlib.PosixPath
    """

    def __init__(self, inputFile):
        if not isinstance(inputFile, str):
            raise TypeError('Parameter inputFile must be of type str')

        with open(inputFile, 'r', newline='\n') as f_open:
            logdata = f_open.read().replace('\r', '')

        start_data = 'Per MPI rank'
        end_data = 'Loop time'
        fix_halt = 'Fix halt'
        self.thermo_dict = {}

        # Reducing log file by removing multiple spaces and copy of script up to self.start_data
        logdata = re.sub(' +', ' ', logdata)
        logdata = re.sub('\t', ' ', logdata)
        logdata = logdata[[m.start() for m in re.finditer(
            start_data, logdata)][0]:]

        # Finding indices for the start of the line above the thermo data
        ind_line_above_thermo = [
            m.start() for m in re.finditer(start_data, logdata)]

        # Number of thermo datasets
        self.No_thermo = len(ind_line_above_thermo)

        # Index of column titles
        ind_thermo_titles_start = [
            logdata.find('\n', ind_line_above_thermo[i]) + 1
            for i in range(self.No_thermo)
        ]

        # Storing titles to use as keys in dictionary
        ind_thermo_titles_stop = logdata.find(
            '\n', ind_thermo_titles_start[0]
        )
        thermo_titles = logdata[
            ind_thermo_titles_start[0]:ind_thermo_titles_stop
        ].split()

        No_columns = len(thermo_titles)

        ind_thermo_start = [
            logdata.find('\n', ind_thermo_titles_start[i]) + 1
            for i in range(self.No_thermo)
        ]

        # Finding indices for the start of the line above and below the thermo data
        ind_line_below_thermo = [
            m.start() - 2 for m in re.finditer(end_data, logdata)]  # -2 to remove \n and space

        halt = logdata.find(fix_halt, ind_thermo_start[-1])

        if halt != -1:
            if len(ind_line_below_thermo) == len(ind_thermo_start):
                ind_line_below_thermo[-1] = halt - 1
            elif len(ind_line_below_thermo) < len(ind_thermo_start):
                ind_line_below_thermo.append(halt - 1)

        if len(ind_line_below_thermo) < len(ind_thermo_start):
            # If there is no end detected (typically MPI_Abort / time ran out)
            ind_line_below_thermo.append(-1)

        self.thermo_dict = {key: [] for key in thermo_titles}
        for i in range(self.No_thermo):
            lines = logdata[
                ind_thermo_start[i]:ind_line_below_thermo[i]
            ].split('\n')

            for line in lines:
                elms = line.split()
                for key, elm in zip(thermo_titles, elms):
                    self.thermo_dict[key].append(np.float(elm))

    def __call__(self):
        """Returns the dictionary containing log file columns.

        :returns thermo_dict: Columns of log file
        :rtype thermo_dict: dict
        """
        return self.thermo_dict

    def get(self, data):
        """Returns a specific column from the log file.

        :param obj: Specifies which values from log file to extract
        :type obj: str
        :returns values: Corresponding values of parameters data
        :rtype values: list
        """
        if not isinstance(data, str):
            raise TypeError(
                f'Argument obj is of type {type(data)}, must be of type str')
        return self.thermo_dict[data]

    def get_thermos(self):
        """Returns the headers of the columns of data, i.e. what thermodynamic
        data has been found present in the logfile.

        :returns headers: Headers of the columns of thermo data
        :rtype headers: list
        """
        headers = self.thermo_dict.keys()
        return headers
