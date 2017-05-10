# XCode Command-line Tools Installer

The `xcode-cltools-installer` allows you to install the XCode Command-line
Tools from a Disk Image File (`.dmg`) to a directory of your choice. This
gives you access to all available Command-line Tools, even old ones that would
normally not install on a newer version of macOS.

    $ xcode-cltools-installer install ~/Downloads/xcode8.2-10.12-2016.12.13.dmg ~/Applications/ClTools-8.2
    $ source ~/Applications/ClTools-8.2/activate
    $ clang --version

## Installation

1. Make sure you have Python 2 or 3 installed on your system.
2. Make sure you have [Pip] installed, otherwise run [get-pip.py].
3. Install [Node.py] via Pip: `sudo pip install node.py`
4. Install the XCode CLTools Installer via PPYM:
   `ppym install --global xcode-cltools-installer`

> **Note**. For XCode Disk Image Files from version 8.0 and higher, [pbzx] is
> needed and will be downloaded if not available. The location that XCode
> CLTools Installer will be installed to via PPYM must be writable by the user
> running it (which it usually is when using `--global`) or otherwise
> `xcode-cltools-installer getpbzx` needs to be called by the user that
> installed it with `--root`.

  [Node.py]: https://github.com/nodepy/nodepy
  [pbzx]: https://github.com/NiklasRosenstein/pbzx
  [Pip]: https://github.com/pypa/pip
  [get-pip.py]: https://bootstrap.pypa.io/get-pip.py
  [Apple Developer Downloads]: https://developer.apple.com/downloads/index.action
  [XCode Version Table]: https://github.com/NiklasRosenstein/xcode-cltools-installer/wiki/XCode-Versions

## Additional Links

- [Apple Developer Downloads]
- [XCode Version Table]

## Changelog

__v1.0.4__

- Add missing `"bin"` field to `package.json`

__v1.0.3__

- Must now be used with [Node.py](https://github.com/nodepy/nodepy)
- Update command-line interface with Click
- Using `sudo` for the `install` command is no longer a requirement, but will
  lead to some files not being extracted (usually man page files)
- Fix `getversion` command -- but still extracts full disk image
- Add `getpbzx` command
- `pbzx` will now be automatically downloaded if it is not available

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

