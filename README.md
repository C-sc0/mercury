# Description
This tool is a multi tasking tool focused in gather information about a network or web site.

## INSTALLATION

1. The first you need to do is clone the repository using `git clone [REPOSITORY_URL]`.

2. After that, go to the downloaded directory.
3.  **^OPTIONAL^** Create a virtual enviroment. [HOW TO CREATE A VIRTUAL ENVIROMENT](https://www.geeksforgeeks.org/creating-python-virtual-environment-windows-linux/) **^OPTIONAL^**
4. and run `python -m pip install -r ./requirements.txt`.

3. **Thats all, now run the tool!**


## USAGE

1. run `python ./main.py -e`
2. and choose the script you want to run and fill the next field or fields.

### NOTE
Some features (Like Scapy library) needs superuser privilege, so, you have to run your terminal as ADMINISTRATOR in Windows or run `sudo` before `python ./main.py -e` in Linux.


## SCRIPTS

###### == NETWORKING ==
1. `host_disc`: Choose the `0` option to scan a network or a single target and discover which are online.
2. `os_disc`: Choose the `1` option to discover which operating system is running in a online host.

###### == WEB ==
3. `web_disc`: Choose the `2` option to get basic information about a web site.
4. `services_in_web`: Choose the `3` option to get services, versión and category running in a web site.

###### == OPERATING SYSTEM ==
3. `extract_wlan_passwords`: Choose the `4` option to list all WLAN connetions and show passwords stored in the operating system.


## COMMANDS

1. run `python ./main.py -h` to show the help panel.
2. run `python ./main.py -v` to show the version of Mercury.
3. run `python ./main.py -e` to list the tools.
4. run `python ./main.py -S` to show all scripts options.
