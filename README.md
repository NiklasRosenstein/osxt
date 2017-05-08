# XCode CLTools Installer

Welcome! This repository contains a script to install the XCode CommandLine
Tools into a directory of your choice, including a script to activate the tools
in your terminal.

    $ clang --version
    Apple LLVM version 8.0.0 (clang-800.0.42.1)
    Target: x86_64-apple-darwin16.0.0
    Thread model: posix
    InstalledDir: /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin
    $ source xcode6.0-10.09-2014.09.02.dmg/activate
    $ clang --version
    Apple LLVM version 6.0 (clang-600.0.51) (based on LLVM 3.5svn)
    Target: x86_64-apple-darwin16.0.0
    Thread model: posix

## Usage

You node [Node.py] installed. Then you can install the XCode CLTools Installer
from GitHub using Node.py's package manager PPYM.

    $ sudo pip install node.py
    $ ppym install --global git+https://github.com/NiklasRosenstein/xcode-cltools-installer.git

The script requires [pbzx], but it will be downloaded automatically if it
is not available. Now you only have to grab yourself an XCode CLTools Disk
Image File from the [Apple Developer Downloads] page. You might want to add
sudo if you also want manpage files.

    $ xcode-cltools-installer install <image.dmg> <dest>

After all the files have been extracted, you can activate the command-line
tools using the `activate` script that was placed into the `<dest>` directory.

    $ source <dest>/activate
    $ clang --version

  [Apple Developer Downloads]: https://developer.apple.com/downloads/index.action
  [XCode Version Table]: https://github.com/NiklasRosenstein/xcode-cltools-installer/wiki/XCode-Versions
  [Node.py]: https://github.com/nodepy/nodepy
  [pbzx]: https://github.com/NiklasRosenstein/pbzx

## Links

- [Apple Developer Downloads]
- [XCode Version Table]

## Changelog

__v1.0.3__

- Using `sudo` for `./install` is no longer a requirement, but will lead to
  some files not being extracted (usually man page files).
- Fix `./getversion` -- but still extracts full disk image
- Update command-line interface with Click
- Must now be used with [Node.py](https://github.com/nodepy/nodepy)

__v1.0.2__

- Add `--debug-pkg` argument
- Removed `--no-sdk` and `--no-cltools` command-line options, all components
  of the Disk Image will now be unpacked into the target folder
- If `--owner` is not specified, `./install` will now automatically figure
  the user and group ID of the user that run the command with `sudo`

__v1.0.1__

- Fix newer DMGs where the `.pkg` files are not actually files but directories
  (see #9 and #5)

__v1.0.0__

- Initial release

---

<p align="center"><i>Copyright (C) 2014-2017 Niklas Rosenstein</i></p>

