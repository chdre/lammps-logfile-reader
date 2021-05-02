import numpy as np
import pandas as pd
import re
import json


class readLog:
    """Read a LAMMPS logfile.
    """

    def __init__(self, inputFile):
        """
        Arguments:
            inputFile (str): Full path to logfile.
        """
        self.start_data = 'Per MPI rank'
        self.end_data = 'Loop time'
        self.fix_halt = 'Fix halt'
        self.thermo_dict = {}

        with open(inputFile, 'r', newline='\n') as f_open:
            self.logdata = f_open.read().replace('\r', '')

        # Reducing log file by removing multiple spaces and copy of script up to self.start_data
        self.logdata = re.sub(' +', ' ', self.logdata)
        self.logdata = re.sub('\t', ' ', self.logdata)
        self.logdata = self.logdata[[m.start() for m in re.finditer(
            self.start_data, self.logdata)][0]:]

        # Finding indices for the start of the line above the thermo data
        ind_line_above_thermo = [
            m.start() for m in re.finditer(self.start_data, self.logdata)]

        # Number of thermo datasets
        self.No_thermo = len(ind_line_above_thermo)

        # Index of column titles
        ind_thermo_titles_start = [
            self.logdata.find('\n', ind_line_above_thermo[i]) + 1
            for i in range(self.No_thermo)]

        # Storing titles to use as keys in dictionary
        ind_thermo_titles_stop = self.logdata.find(
            '\n', ind_thermo_titles_start[0])
        self.thermo_titles = self.logdata[
            ind_thermo_titles_start[0]:ind_thermo_titles_stop
        ].split()

        No_columns = len(self.thermo_titles)

        self.ind_thermo_start = [
            self.logdata.find('\n', ind_thermo_titles_start[i]) + 1
            for i in range(self.No_thermo)]

        # Finding indices for the start of the line above and below the thermo data
        self.ind_line_below_thermo = [
            m.start() - 2 for m in re.finditer(self.end_data, self.logdata)]  # -2 to remove \n and space

        halt = self.logdata.find(self.fix_halt, self.ind_thermo_start[-1])

        if halt != -1:
            if len(self.ind_line_below_thermo) == len(self.ind_thermo_start):
                self.ind_line_below_thermo[-1] = halt - 1
            elif len(self.ind_line_below_thermo) < len(self.ind_thermo_start):
                self.ind_line_below_thermo.append(halt - 1)

        if len(self.ind_line_below_thermo) < len(self.ind_thermo_start):
            # If there is no end detected (typically MPI_Abort / time ran out)
            self.ind_line_below_thermo.append(-1)

        return

    def datadict(self):
        """Creates dictionary containing information from logfile.

        Returns:
            self.thermo_dict (dict): Dictionary containing columns of logfile.
        """
        self.thermo_dict = {key: [] for key in self.thermo_titles}
        for i in range(self.No_thermo):
            lines = self.logdata[
                self.ind_thermo_start[i]:self.ind_line_below_thermo[i]
            ].split('\n')

            for line in lines:
                elms = line.split()
                for key, elm in zip(self.thermo_titles, elms):
                    self.thermo_dict[key].append(elm)

        return self.thermo_dict
