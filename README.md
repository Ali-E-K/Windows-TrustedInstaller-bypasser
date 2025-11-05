## TI-Bypasser

A tool that lets you execute commands on your Windows computer without interference from TrustedInstaller or other restrictions.

#### Requirements

- Python 3.6+ (Not required to be installed for the executable)
- subprocess (Built in. Not required to be installed for the executable)
- sys (Built in. Not required to be installed for the executable)
- ctypes (Built in. Not required to be installed for the executable)
- time (Built in. Not required to be installed for the executable)
- tkinter (Built in. Not required to be installed for the executable)

#### The following requirements will be installed automatically by the program after you have been asked for permission

- NuGet 2.8.5.201+
- NtObjectManager 1.1.32+

#### Usage

Run the executable `ti_bypasser.exe`

Or run the following command in a command prompt:

```sh
python main.py
```

```sh
ti_bypasser.exe
```

To troubleshoot errors, run the following command to keep the console open and examine the output
(Some command prompts may not close even without the "debug" argument):

```sh
python main.py debug
```

or:

```sh
ti_bypasser.exe debug
```
