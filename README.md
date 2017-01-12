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

1. Clone this repository including submodules.

        git clone --recursive https://github.com/NiklasRosenstein/xcode-cltools-installer.git

2. Build `pbzx` which is required to unpack later Disk Images (from OSX 10.10).

       clang -llzma -lxar -I /usr/local/include pbzx/pbzx.c -o pbzx/pbzx

3. Download an XCode CL-Tools Disk Image from the [Apple Developer Downloads] page.

4. Use `sudo ./install <image.dmg> <dest>` to install the developer tools.

    > Note: if you do not use `sudo`, some files might not be extracted
    > (usually man pages).

5. Activate the tools with `source <dest>/activate`.

  [Apple Developer Downloads]: https://developer.apple.com/downloads/index.action
  [pbzx]: https://github.com/NiklasRosenstein/pbzx
  [XCode Version Table]: https://github.com/NiklasRosenstein/xcode-cltools-installer/wiki/XCode-Versions


## Links

- [Apple Developer Downloads]
- [XCode Version Table]

## Changelog

__v1.0.3__

- Using `sudo` for `./install` is no longer a requirement, but will lead to
  some files not being extracted (usually man page files).
- Fix `./getversion` -- but still extracts full disk image

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

