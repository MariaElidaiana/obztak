# MagLiteS

Bizarro Observation Tactician (ObzTak) for the **Mag**ellanic Satel**lite**s **S**urvey (MagLiteS).

* Contact: Keith Bechtol <keith.bechtol@icecube.wisc.edu>
* Contact: Alex Drlica-Wagner <kadrlica@fnal.gov>

### Installation

### Running

The first step is to run `prepare_survey` to set up the necessary survey characterization files. Specifically, this script builds a list of survey fields and a list of expected time windows. These files will be written to the current directory by default.
```
> ./bin/prepare_survey --help
usage: prepare_survey [-h] [-p] [-f FIELDS] [-w WINDOWS]

Decide which fields to observe and time windows to observe.

optional arguments:
  -h, --help            show this help message and exit
  -p, --plot            Plot output. (default: False)
  -f FIELDS, --fields FIELDS
                        List of all target fields. (default:
                        target_fields.txt)
  -w WINDOWS, --windows WINDOWS
                        List of observation windows. (default:
                        observation_windows.txt)
```


There are two pimary executables: `survey_simulator` and `survey_observer`. Both use the same underlying architecture, but the `survey_simulator` simulates the entire survey while `survey_observer` is used to simulate only a specific chuck of the survey and create an output json file. Both have the `-p` option for real-time plotting.
```
> ./bin/survey_simulator --help
usage: survey_simulator [-h] [-v] [-p] [-fields FIELDS] [-w WINDOWS] [-d DONE]
                        [-o OUTFILE]

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Output verbosity.
  -p, --plot            Plot output.
  -fields FIELDS, --fields FIELDS
                        List of all target fields.
  -w WINDOWS, --windows WINDOWS
                        List of observation windows.
  -d DONE, --done DONE  List of fields that have been observed.
  -o OUTFILE, --outfile OUTFILE
                        Save output fields surveyed.
```

```
usage: survey_observer [-h] [-v] [-p] [-fields FIELDS] [-w WINDOWS] [-d DONE]
                       [-o OUTFILE] [--tstart TSTART] [--tstop TSTOP]

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Output verbosity.
  -p, --plot            Plot output.
  -fields FIELDS, --fields FIELDS
                        List of all target fields.
  -w WINDOWS, --windows WINDOWS
                        List of observation windows.
  -d DONE, --done DONE  List of fields that have been observed.
  -o OUTFILE, --outfile OUTFILE
                        Save output fields surveyed.
  --tstart TSTART       Start time for observation.
  --tstop TSTOP         Stop time for observation.
```

## Installation

### To clone repository ###

* Go to the directory where you want to work
* git clone https://username@bitbucket.org/bechtol/maglites.git # Substitute your own username

### Keeping your local copy up to date ###

* git pull --all # git pull moves changes from the remote repository to your local copy

### To commit an update ###

* git add example.txt # git add command moves changes from the working directory to the staging area
* git commit -m 'my comments' # git commit takes the staged snapshot and commits it to the project history
* git push -u origin master # git push moves a local branch or series of commits to main repository

### More git documentation ###

* https://confluence.atlassian.com/display/BITBUCKET/Clone+your+Git+repository+and+add+source+files
* https://confluence.atlassian.com/display/BITBUCKET/Create+a+file+and+pull+changes+from+Bitbucket