# XCode CLTools Installer

Welcome! This repository contains a script to install the XCode CommandLine
Tools into a directory of your choice, including a script to activate the tools
in your terminal.

    $ clang --version
    Apple LLVM version 8.0.0 (clang-800.0.42.1)
    Target: x86_64-apple-darwin16.0.0
    Thread model: posix
    InstalledDir: /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin
    $ source OSX10.09-2014-09-02/activate
    $ clang --version
    Apple LLVM version 6.0 (clang-600.0.51) (based on LLVM 3.5svn)
    Target: x86_64-apple-darwin16.0.0
    Thread model: posix


## Installation

1. Clone this repository (`git clone https://github.com/NiklasRosenstein/xcode-cltools-installer.git`)
2. Download an XCode CL-Tools Disk Image from the [Apple Developer Downloads] page.
2. Use `sudo ./install <image.dmg> <dest>` to install the developer tools
3. Activate the tools with `source <dest>/activate`

[Apple Developer Downloads]: https://developer.apple.com/downloads/index.action


## Links

- [Apple Developer Downloads]


## Compiler Versions

Here's a list about which compiler version you can find in which package of the
XCode Command Line Tools and for which versions of OSX the tools used to be
available. Usually you can still use old command-line tools on newer versions
of OSX using the approach encouraged by this repository.

__Clang 5.0__

- September 16, 2013 (Mountain Lion) (clang-500.2.75)
- October 22, 2013 (Mavericks, Mountain Lion) (clang-500.2.79)

__Clang 5.1__

- March 10, 2014 (Mavericks, Mountain Lion) (clang-503.0.38)
- April 10, 2014 (Mavericks, Mountain Lion) (clang-503.0.40)

__Clang 6.0__

- September 02, 2014 (Mavericks) (clang-600.0.51)

__Todo__

All images since *July 07, 2014* still need to be analysed.


## Changelog

__v1.0.2__

- Add `--debug-pkg` argument

__v1.0.1__

- Fix newer DMGs where the `.pkg` files are not actually files but directories
  (see #9 and #5)

__v1.0.0__

- Initial release

---

<p align="center"><i>Copyright (C) 2014-2017 Niklas Rosenstein</i></p>

