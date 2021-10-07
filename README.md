# lammps-logfile-reader
A simple program to read log files generated by LAMMPS. Supports breaking conditions under the condition that they are named "Fix halt", as in LAMMPS documentation.

Creates an object containing the information in the logfile, stored in as dictionaries. To access data 

# Requirements
* pandas
* regex

# Usage
```
from read_lammps_log.py import readLog

path = 'some/path/log.lammps'
variable = 'Temp'

log_reader = readLog(path)
temperature = log_reader.get(variable)
```

To get full list of keys (thermo_style)
```
termo_style = log_reader.keys()
```


# To-do
- Add user customisability for halting condition
- Create pypi package
- Create tests
