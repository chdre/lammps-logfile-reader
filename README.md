# lammps-logfile-reader
A simple program to read log files generated by LAMMPS. Supports breaking conditions under the condition that the condition is a fix and named "halt", as per the LAMMPS documentation.

Reads LAMMPS logfiles and stores information in a dictionary. All values are converted to float. To access data use .get() as standard with Python dictionaries, where the argument corresponds to the variable of which you wish to read data.

# Requirements
* regex

# Install
Install using pip
```
pip install git+https://github.com/chdre/lammps-logfile-reader
```

# Usage
```
from lammps_logfile_reader import ReadLog ReadLog

path = '.../log.lammps'

logdict = ReadLog(path)

variable = 'Temp'

temperature = logdict.get(variable)
```

To get full list of headers of columns of thermodynamic data:
```
headers = logdict.get_thermos()
```
or by standard dictionary operations
```
headers = logdict().keys()
```


# To-do
- Add user customisability for halting condition
- Create tests
