XCode - Local CLTools Installation
==================================

This repository contains a script to install the XCode CommandLine Tools
into a specific directory. The script must be run as superuser because
unpacking the Mac OS SDK contains files that can not be extracted without
root permissions.

    sudo ./install.py \
        ~/Downloads/command_line_tools_os_x_mavericks_for_xcode__late_october_2013.dmg \
        ~/CLTools/Clang-5.0 \
        --owner niklas

After it has completed, you can activate the CLTools.

    source ~/CLTools/Clang-5.0/activate

-----

    usage: install.py [-h] [-o OWNER] [-f FORCE] archive dest

    Install Mac OS Command Line Tools to a specific directory. Note that the
    script must be run as superuser to unpack all files from the Mac OS X SDK
    without problems. The script will exit immediately if not run as superuser.

    positional arguments:
      archive               The archive that contains the Command Line Tools which
                            must be a *.dmg file.
      dest                  The destination output folder. The Command Line Tools
                            will be installed to this folder and a script to
                            activate the tools will be put there as well.

    optional arguments:
      -h, --help            show this help message and exit
      -o OWNER, --owner OWNER
                            The new owner of the expanded files. Since you need to
                            call this script as superuser, the it can not
                            determine by itself what user you are.
      -f FORCE, --force FORCE
                            Force overwrite if the directory already exists.
                            Otherwise, you will be prompted in the console.

__Copyright (C) 2014 Niklas Rosenstein__
