# Summary

This script intends to update the EPI week/year TEA for all the no-legacy TEI registered in AFP & MR program.

The script is only taking into account the new/updated TEI since the last time execution. In order to save the last
execution time for each program, 2 log files (XXXXXX_runtime.log) needs to be installed in the same location of the
script.

## Input files

- `{PROGRAM_UID}_runtime.log` Log file to save last script execution time of each program (AFP & MR)
- `credentials.ini` File to keep credentials and setup variables

## Output files

- `dhis2_epiweek.log` Log file.

## Getting Started

To use this script, you will need to have `Python3` installed on your system.

### Steps

1. Rename `credentials-template.ini` to `credentials.ini` and adjust the following variables corresponding to the
   running environment:
    - `server_url` = Point to the server URL where you're running the script
    - `dhis2_username` = username
    - `dhis2_password` = password
    - `runtime_log_path` = Point to the server path where the runtime log files are saved
    - `log_file` = /xxxx/xxx/dhis2_epiweek.log
2. Select the credentials that you want to use.
    - In function `set_credentials()`, line `params = parser.items("paho_vpd_local")`, change the fixed value of
      `paho_vpd_local` with the desired environment from `credentials.ini`.
3. Run the script
4. Check the log file

## Run

Once the dependencies have been installed, you have to navigate to the script directory path and run the script by
running:

`python DHIS2_EPI_WEEK.py`

## Notes

- In order to execute the script, It's recommended to create a specific DHIS2 user with minimum authorities (user
  role & user groups).
    - Recommended settings are
        - User: `cron`
        - User role: `VPD - Cron` with tracker authorities:
            - Search Tracked Entity Instance in All Org Units
            - Update tracked entities
        - User groups: `VPD - MR - Users Full` & `VPD - AFP - Users Full`
- In `credentials.ini`, while running the script in a server, you should set:
    - `runtime_log_path=/opt/pythonapps/`
    - `log_file=/var/log/dhis2_epiweek/dhis2_epiweek.log`
- Log files are saved under path `/var/log/dhis2_epiweek/dhis2_epiweek.log`
- In step 2, while running the script from your local machine, you should edit function `set_credentials()`, line
  `parser.read("/opt/pythonapps/credentials.ini")`, change the line with `parser.read("credentials.ini")`.
- In order to calculate the EPI week and year for each TEI, we use:
    - For onset attribute we use `enrollment_date = enrolledAt`
    - For notification attribute we use `incident_date = occurredAt`