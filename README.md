# captain-ahab
Captain ahab handles your fishing needs

## Installation
A virtualenv is suggested.  Python 3.6+ is required.
```
# Powershell
> python -m venv .venv
> . .venv/Scripts/Activate.ps1
> pip install git+https://github.com/wnormandin/captain-ahab.git

# Bash
$ python -m venv .venv
$ . .venv/bin/activate
$ pip install git+https://github.com/wnormandin/captain-ahab.git
```

## Configuration

A configuration file path may be specified using the `CAPTAIN_AHAB_CONFIG` environment variable.  This will default
to `pequod.ini`.  See `pequod.ini` in the project root for a sample configuration file.

To fetch the sample ini:
```
# Powershell
> Invoke-WebRequest -Uri "https://raw.githubusercontent.com/wnormandin/captain-ahab/main/pequod.ini" -OutFile "%HOME%\pequod.ini"
> $env:CAPTAIN_AHAB_CONFIG="%HOME%\pequod.ini"

# Bash
$ curl -sk https://raw.githubusercontent.com/wnormandin/captain-ahab/main/pequod.ini > ~/pequod.ini
$ export CAPTAIN_AHAB_CONFIG="~/pequod.ini"
```

### Example Configuration
```
[captain]
# flag indicating whether to invoke "test mode"
test = yes

# max verbosity value=3
verbosity = 3

# When set, save a copy of the sample image each time one is taken
sample_image_path = sample.png

[sample_dimensions]
# Sample rectangle x starting pixel
x = 250

# Sample rectangle y starting pixel
y = 250

# Sample width, in pixels
w = 1300

# Sample height, in pixels
h = 1300

[logging]
# valid values: DEBUG, INFO, WARNING, ERROR, CRITICAL
log_level = DEBUG

# When set, save log entries at the given path
log_file = captainslog.txt
```

## Running the captain