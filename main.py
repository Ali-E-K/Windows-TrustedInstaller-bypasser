# The code does not bypass TrustedInstaller, but it achieves the same effect.
try:
    import subprocess as sp
    import sys
    import ctypes
    import time
    import tkinter.messagebox as mb


    # If the script does not have administrator privileges, ask for them.
    if not ctypes.windll.shell32.IsUserAnAdmin():
        # Ask for administrator privileges.
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, f'\" \"'.join(sys.argv),
            None, 1)
        sys.exit(0)

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

    # Install the necessary module if it cannot be found.
    check_module = sp.run(["powershell", "-Command", "Import-Module", "NtObjectManager"], stdout=sys.stdout,
                          stderr=sp.PIPE)
    check_module = check_module.stderr.decode("utf-8")

    if "Modules_ModuleNotFound" in check_module:
        print("Installing module...")
        sp.run(["powershell", "-Command", "Install-Module", "NtObjectManager", "-RequiredVersion", "1.1.32"],
               stdout=sys.stdout, stderr=sys.stderr)

    # It is not possible to see if TrustedInstaller is running or not so try to close it even if it's not running.
    sp.run(["powershell", "-Command", "sc.exe", "stop", "TrustedInstaller"], stdout=sys.stdout,
           stderr=sys.stderr)


    # Open a terminal that lets you execute commands as the TrustedInstaller.
    sp.run(["powershell", "-Command", "sc.exe", "start", "TrustedInstaller;", "Import-Module", "NtObjectManager;",
            "$p", "=", "Get-NtProcess", "TrustedInstaller.exe;"
            "New-Win32Process", "cmd.exe", "-CreationFlags", "NewConsole", "-ParentProcess", "$p[-1]"],
           stderr=sys.stderr, stdout=sys.stdout)

    time.sleep(1)

    sp.run(["powershell", "-Command", "Set-ExecutionPolicy", exe_policy], stdout=sys.stdout, stderr=sys.stderr)

    if "debug" in sys.argv:
        print("Process completed. Press Enter to exit...")
        input()
except Exception as e:
    print(f"An error occurred\n{e}\nPress Enter to exit...")
    input()
