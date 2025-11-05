# The code doesn't actually bypass TrustedInstaller. However it achieves the
# same effect by opening a terminal and disguising it as TrustedInstaller
try:
    import subprocess as sp
    import sys
    import ctypes
    import time
    import tkinter.messagebox as mb
    import tkinter as tk


    # If the script does not have administrator privileges.
    if not ctypes.windll.shell32.IsUserAnAdmin():
        # Ask for administrator privileges.
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable,
            '\"' + sys.argv[0] + '\"' + " " + " ".join(sys.argv[1:]), None, 1)
        sys.exit(0)

    # When using tkinter.messagebox a hidden Tk main window is opened.
    # In some cases the window may not be hidden. Manually create and hide
    # the main window to avoid this error.
    bug_stopper = tk.Tk()
    bug_stopper.withdraw()

    confirmation = mb.askyesno("Warning", "This script will temporarily modify your computers execution policy and" +
                               " may introduce security risks. by the time your terminal is ready to use these risks "
                               + "will be terminated. Do you want to continue?")

    if not confirmation:
        sys.exit(0)

    # Make sure powershell will allow us to import a module.
    # (The execution policy will be set back to its original state at the end of the script.)
    exe_policy = sp.run(["powershell", "-Command", "Get-ExecutionPolicy"], stdout=sp.PIPE, stderr=sys.stderr)
    exe_policy = exe_policy.stdout.decode("utf-8")

    if exe_policy != "Unrestricted":
        sp.run(["powershell", "-Command", "Set-ExecutionPolicy", "Unrestricted"], stdout=sys.stdout,
               stderr=sys.stderr)

    del_module = False
    # Install the necessary module if it cannot be found.
    check_module = sp.run(["powershell", "-Command", "Import-Module", "NtObjectManager"], stdout=sys.stdout,
                          stderr=sp.PIPE)
    check_module = check_module.stderr.decode("utf-8")


    if "Modules_ModuleNotFound" in check_module:
        confirmation = mb.askyesnocancel("Info", "Necessary module not found and will be installed. Would you" +
                                   "like to delete it after on?")
        if confirmation == None:
            sys.exit(0)

        del_module = confirmation
        print("Installing module...")
        sp.run(["powershell", "-Command", "Install-Module", "NtObjectManager", "-RequiredVersion", "1.1.32"],
               stdout=sys.stdout, stderr=sys.stderr)


    # Enter the TrustedInstaller's path
    sp.run(["powershell", "-Command", "sc.exe", "config", "TrustedInstaller",
            'binpath=\"C:\\Windows\\servicing\\TrustedInstaller.exe\"'])

    # It is not possible to see if TrustedInstaller is running or not so try to close it even if it's not running.
    sp.run(["powershell", "-Command", "sc.exe", "stop", "TrustedInstaller"], stdout=sys.stdout,
           stderr=None)


    # Open a terminal that lets you execute commands as the TrustedInstaller.
    sp.run(["powershell", "-Command", "sc.exe", "start", "TrustedInstaller;", "Import-Module", "NtObjectManager;",
            "$p", "=", "Get-NtProcess", "TrustedInstaller.exe;"
            "New-Win32Process", "cmd.exe", "-CreationFlags", "NewConsole", "-ParentProcess", "$p[-1]"],
           stderr=sys.stderr, stdout=sys.stdout)

    time.sleep(1)

    sp.run(["powershell", "-Command", "Set-ExecutionPolicy", exe_policy], stdout=sys.stdout, stderr=sys.stderr)
    if del_module:  # Delete the installed module if the user wants to
        sp.run(["powershell", "-Command", "Uninstall-Module", "NtObjectManager"], stdout=sys.stdout, stderr=sys.stderr)

    if "debug" in sys.argv:
        print("Process completed. Press Enter to exit...")
        input()
except Exception as e:
    print(f"An error occurred:\n{e}\nPress Enter to exit...")
    input()
