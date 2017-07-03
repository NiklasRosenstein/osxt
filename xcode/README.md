# XCode Command-line Tools Installer

This application allows you to download and install the XCode Command-line
Tools from a Disk Image File (`.dmg`) to a directory of your choice. This
gives you access to all available Command-line Tools, even old ones that would
normally not install on a newer version of macOS.

    >_ osxt xcode
    Usage: osxt xcode [OPTIONS] COMMAND [ARGS]...

      Download and install XCode CommandLine Tools.

    Options:
      --help  Show this message and exit.

    Commands:
      download    Download a file from the Apple Developer...
      getpbzx     Checks if pbzx is available, otherwise...
      getversion  Installs to a temporary directory and outputs...
      install     Create a local installation of the Mac OS...

---

<table><tr>
<td>CLI</td><td>Download</td><td>Install</td><td>Usage</td>
</tr><tr>
<td><img src="http://i.imgur.com/TnlDqiL.png" align="center"></td>
<td><img src="http://i.imgur.com/WD2C7kc.png" align="center"></td>
<td><img src="http://i.imgur.com/nx6vj6X.png" align="center"></td>
<td><img src="http://i.imgur.com/EFfdyaB.png" align="center"></td>
</tr></table>

---

## Usage

1. Install **osxt** with [Node.py]
2. Download an XClode CLTools image from the [Apple Developer Downloads] page
   or use the `osxt xcode download` command (check the [XCode Version Table]
   below).
3. Use the `osxt xcode install` command.

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
  [XCode Version Table]: #xcode-version-table
  [Changelog]: #changelog

## XCode Version Table

<!-- XCode Version Table Begin -->
| Date YMD | OSX Version | XCode Version | Suggested Image Name | Trunk |
| -------- | ----------- | ------------- | -------------------- | ----- |
| 2017/04/18 | 10.12 (Sierra) | 8.3.2 (LLVM 8.1.0) | [xcode8.3.2-10.12-2017.04.18.dmg](http://adcdownload.apple.com/Developer_Tools/Command_Line_Tools_for_Xcode_8.3.2/CommandLineToolsforXcode8.3.2.dmg) | clang-802.0.42 |
| 2017/03/27 | 10.12 (Sierra) | 8.3 (LLVM 8.1.0) | [xcode8.3-10.12-2017.03.27.dmg](http://adcdownload.apple.com/Developer_Tools/Command_Line_Tools_macOS_10.12_for_Xcode_8.3/Command_Line_Tools_macOS_10.12_for_Xcode_8.3.dmg) | clang-802.0.38 |
| 2016/12/13 | 10.12 (Sierra) | 8.2 | [xcode8.2-10.12-2016.12.13.dmg](http://adcdownload.apple.com/Developer_Tools/Command_Line_Tools_macOS_10.12_for_Xcode_8.2/Command_Line_Tools_macOS_10.12_for_Xcode_8.2.dmg) |
| 2016/12/12 | 10.11 (El Capitan) | 8.2 | [xcode8.2-10.11-2016.12.12.dmg](http://adcdownload.apple.com/Developer_Tools/Command_Line_Tools_macOS_10.11_for_Xcode_8.2/Command_Line_Tools_macOS_10.11_for_Xcode_8.2.dmg) |
| 2016/10/27 | 10.12 (Sierra) | 8.1 | [xcode8.1-10.12-2016.10.27.dmg](http://adcdownload.apple.com/Developer_Tools/Command_Line_Tools_macOS_10.12_for_Xcode_8.1/Command_Line_Tools_macOS_10.12_for_Xcode_8.1.dmg) |
| 2016/09/13 | 10.12 (Sierra) | 8.0 | [xcode8.0-10.12-2016.09.13.dmg](http://adcdownload.apple.com/Developer_Tools/Command_Line_Tools_macOS_10.12_for_Xcode_8/Command_Line_Tools_macOS_10.12_for_Xcode_8.dmg) |
| 2016/05/04 | 10.11 (El Capitan) | 7.3.1 | [xcode7.3.1-10.11-2016.05.04.dmg](http://adcdownload.apple.com/Developer_Tools/Command_Line_Tools_OS_X_10.11_for_Xcode_7.3.1/Command_Line_Tools_OS_X_10.11_for_Xcode_7.3.1.dmg) |
| 2016/03/21 | 10.11 (El Capitan) | 7.3 | [xcode7.3-10.11-2016.03.21.dmg](http://adcdownload.apple.com/Developer_Tools/Command_Line_Tools_OS_X_10.11_for_Xcode_7.3/Command_Line_Tools_OS_X_10.11_for_Xcode_7.3.dmg) |
| 2015/12/08 | 10.11 (El Capitan) | 7.2 | [xcode7.2-10.11-2015.12.08.dmg](http://adcdownload.apple.com/Developer_Tools/Command_Line_Tools_OS_X_10.11_for_Xcode_7.2/Command_Line_Tools_OS_X_10.11_for_Xcode_7.2.dmg) |
| 2015/12/08 | 10.10 (Yosemite) | 7.2 | [xcode7.2-10.10-2015.12.08.dmg](http://adcdownload.apple.com/Developer_Tools/Command_Line_Tools_OS_X_10.10_for_Xcode_7.2/Command_Line_Tools_OS_X_10.10_for_Xcode_7.2.dmg) |
| 2015/10/21 | 10.11 (El Capitan) | 7.1 | [xcode7.1-10.11-2015.10.21.dmg](http://adcdownload.apple.com/Developer_Tools/Command_Line_Tools_OS_X_10.11_for_Xcode_7.1/Command_Line_Tools_OS_X_10.11_for_Xcode_7.1.dmg) |
| 2015/10/21 | 10.10 (Yosemite) | 7.1 | [xcode7.1-10.10-2015.10.21.dmg](http://adcdownload.apple.com/Developer_Tools/Command_Line_Tools_OS_X_10.10_for_Xcode_7.1/Command_Line_Tools_OS_X_10.10_for_Xcode_7.1.dmg) |
| 2015/09/16 | 10.10 (Yosemite) | 7.0 | [xcode7.0-10.10-2015.09.16.dmg](http://adcdownload.apple.com/Developer_Tools/Command_Line_Tools_OS_X_10.10_for_Xcode_7/Command_Line_Tools_OS_X_10.10_for_Xcode_7.dmg) |
| 2015/06/30 | 10.10 (Yosemite) | 6.4 | [xcode6.4-10.10-2015.06.30.dmg](http://adcdownload.apple.com/Developer_Tools/Command_Line_Tools_OS_X_10.10_for_Xcode_6.4/Command_Line_Tools_OS_X_10.10_for_Xcode_6.4.dmg) |
| 2015/05/18 | 10.10 (Yosemite) | 6.3.2 | [xcode6.3.2-10.10-2015.05.18.dmg](http://adcdownload.apple.com/Developer_Tools/Command_Line_Tools_OS_X_10.10_for_Xcode_6.3.2/commandlinetoolsosx10.10forxcode6.3.2.dmg) |
| 2015/04/20 | 10.10 (Yosemite) | 6.3.1 | [xcode6.3.1-10.10-2015.04.20.dmg](http://adcdownload.apple.com/Developer_Tools/Command_Line_Tools_OS_X_10.10_for_Xcode_6.3.1/commandlinetoolsosx10.10forxcode6.3.1.dmg) |
| 2015/04/08 | 10.10 (Yosemite) | 6.3 | [xcode6.3-10.10-2015.04.08.dmg](http://adcdownload.apple.com/Developer_Tools/NEW__Command_Line_Tools_OS_X_10.10_for_Xcode__Xcode_6.3/commandlinetoolsosx10.10forxcode6.3.dmg) |
| 2015/03/07 | 10.09 (Mavericks) | 6.2 | [xcode6.2-10.09-2015.03.07.dmg](http://adcdownload.apple.com/Developer_Tools/Command_Line_Tools_OS_X_10.9_for_Xcode__Xcode_6.2/commandlinetoolsosx10.9forxcode6.2.dmg) |
| 2015/03/06 | 10.10 (Yosemite) | 6.2 | [xcode6.2-10.10-2015.03.06.dmg](http://adcdownload.apple.com/Developer_Tools/Command_Line_Tools_OS_X_10.10_for_Xcode__Xcode_6.2/commandlinetoolsosx10.10forxcode6.2.dmg) |
| 2014/12/02 | 10.10 (Yosemite) | 6.1.1 | [xcode6.1.1-10.10-2014.12.02.dmg](http://adcdownload.apple.com/Developer_Tools/command_line_tools_os_x_10.10_for_xcode__xcode_6.1.1/commandlinetoolsosx10.10forxcode6.1.1.dmg) |
| 2014/12/02 | 10.09 (Mavericks) | 6.1.1 | [xcode6.1.1-10.09-2014.12.02.dmg](http://adcdownload.apple.com/Developer_Tools/command_line_tools_os_x_10.9_for_xcode__xcode_6.1.1/commandlinetoolsosx10.9forxcode6.1.1.dmg) |
| 2014/10/16 | 10.10 (Yosemite) | 6.1 | [xcode6.1-10.10-2014.10.16.dmg](http://adcdownload.apple.com/Developer_Tools/command_line_tools_os_x_10.10_for_xcode__xcode_6.1/command_line_tools_for_osx_10.10_for_xcode_6.1.dmg) |
| 2014/10/16 | 10.09 (Mavericks) | 6.1 | [xcode6.1-10.09-2014.10.16.dmg](http://adcdownload.apple.com/Developer_Tools/command_line_tools_os_x_10.9_for_xcode__xcode_6.1/command_line_tools_for_osx_10.9_for_xcode_6.1.dmg) |
| 2014/09/16 | 10.09 (Mavericks) | 6.0 | [xcode6.0-10.09-2014.09.16.dmg](http://adcdownload.apple.com/Developer_Tools/command_line_tools_os_x_10.9_for_xcode__xcode_6/command_line_tools_for_os_x_10.9_for_xcode_6.dmg) |
| 2014/09/02 | 10.09 (Mavericks) | 6.0 | [xcode6.0-10.09-2014.09.02.dmg](http://adcdownload.apple.com/Developer_Tools/command_line_tools_os_x_10.9_for_xcode__september_2014/command_line_tools_for_osx_10.9_september_2014.dmg) | clang-600.0.51 |
| 2014/08/18 | 10.09 (Mavericks) | ?.? | [xcode?.?-10.09-2014.08.18.dmg](http://adcdownload.apple.com/Developer_Tools/command_line_tools_os_x_10.9_for_xcode__late_august_2014/command_line_tools_for_os_x_mavericks_late_august_2014.dmg) |
| 2014/08/04 | 10.09 (Mavericks) | ?.? | [xcode?.?-10.09-2014.08.04.dmg](http://adcdownload.apple.com/Developer_Tools/command_line_tools_os_x_10.9_for_xcode__august_2014/command_line_tools_os_x_10.9_for_xcode__august_2014.dmg) |
| 2014/07/21 | 10.09 (Mavericks) | ?.? | [xcode?.?-10.09-2014.07.21.dmg](http://adcdownload.apple.com/Developer_Tools/command_line_tools_os_x_10.9_for_xcode__late_july_2014/command_line_tools_for_os_x_mavericks_late_july_2014.dmg) |
| 2014/04/10 | 10.09 (Mavericks) | 5.1 | [xcode5.1-10.09-2014.04.10.dmg](http://adcdownload.apple.com/Developer_Tools/command_line_tools_os_x_mavericks_for_xcode__april_2014/command_line_tools_for_osx_mavericks_april_2014.dmg) | clang-503.0.40 |
| 2014/04/10 | 10.08 (Mountain Lion) | 5.1 | [xcode5.1-10.08-2014.04.10.dmg](http://adcdownload.apple.com/Developer_Tools/command_line_tools_os_x_mountain_lion_for_xcode__april_2014/command_line_tools_for_osx_mountain_lion_april_2014.dmg) | clang-503.0.40 |
| 2014/03/10 | 10.09 (Mavericks) | 5.1 | [xcode5.1-10.09-2014.03.10.dmg](http://adcdownload.apple.com/Developer_Tools/command_line_tools_os_x_mavericks_for_xcode__march_2014/commandline_tools_os_x_mavericks_for_xcode__march_2014.dmg) | clang-503.0.38 |
| 2014/03/10 | 10.08 (Mountain Lion) | 5.1 | [xcode5.1-10.08-2014.03.10.dmg](http://adcdownload.apple.com/Developer_Tools/command_line_tools_os_x_mountain_lion_for_xcode__march_2014/commandline_tools_os_x_mountain_lion_for_xcode__march_2014.dmg) | clang-503.0.38 |
| 2013/10/22 | 10.09 (Mavericks) | 5.0 | [xcode5.0-10.09-2013.10.22.dmg](http://adcdownload.apple.com/Developer_Tools/command_line_tools_os_x_mavericks_for_xcode__late_october_2013/command_line_tools_os_x_mavericks_for_xcode__late_october_2013.dmg) | clang-500.2.79 |
| 2013/10/14 | 10.08 (Mountain Lion) | ?.? | [xcode?.?-10.08-2013.10.14.dmg](http://adcdownload.apple.com/Developer_Tools/command_line_tools_os_x_mountain_lion_for_xcode__october_2013/command_line_tools_os_x_mountain_lion_for_xcode__october_2013.dmg) |
| 2013/09/18 | 10.08 (Mountain Lion) | 5.0 | xcode5.0-10.08-2013.09.18.dmg |
| 2013/08/30 | 10.08 (Mountain Lion) | ?.? | [xcode?.?-10.08-2013.08.30.dmg](http://adcdownload.apple.com/Developer_Tools/command_line_tools_os_x_mountain_lion_for_xcode__september_2013/command_line_tools_os_x_mountain_lion_for_xcode__september_2013.dmg) |
| 2013/04/12 | 10.07 (Lion) | ?.? | [xcode?.?-10.07-2013.04.12.dmg](http://adcdownload.apple.com/Developer_Tools/command_line_tools_os_x_lion_for_xcode__april_2013/xcode462_cltools_10_76938260a.dmg) |
| 2013/04/11 | 10.08 (Mountain Lion) | ?.? | [xcode?.?-10.08-2013.04.11.dmg](http://adcdownload.apple.com/Developer_Tools/command_line_tools_os_x_mountain_lion_for_xcode__april_2013/xcode462_cltools_10_86938259a.dmg) |
| 2013/03/14 | 10.08 (Mountain Lion) | ?.? | [xcode?.?-10.08-2013.03.14.dmg](http://adcdownload.apple.com/Developer_Tools/command_line_tools_os_x_mountain_lion_for_xcode__march_2013/xcode461_cltools_10_86938245a.dmg) |
| 2013/03/14 | 10.07 (Lion) | ?.? | [xcode?.?-10.07-2013.03.14.dmg](http://adcdownload.apple.com/Developer_Tools/command_line_tools_os_x_lion_for_xcode__march_2013/xcode461_cltools_10_76938246a.dmg) |
| 2013/01/25 | 10.08 (Mountain Lion) | ?.? | [xcode?.?-10.08-2013.01.25.dmg](http://adcdownload.apple.com/Developer_Tools/command_line_tools_os_x_mountain_lion_for_xcode__january_2013/xcode46cltools_10_86938131a.dmg) |
| 2013/01/25 | 10.07 (Lion) | ?.? | [xcode?.?-10.07-2013.01.25.dmg](http://adcdownload.apple.com/Developer_Tools/command_line_tools_os_x_lion_for_xcode__january_2013/xcode46cltools_10_76938132a.dmg) |
<!-- XCode Version Table End -->

---

## Changelog

- Merged into [osxt](https://github.com/NiklasRosenstein/osxt)

__v1.0.5__

- Add `download` subcommand, allowing you to select the image to download
- Now requires `prompt_toolkit` (automatically installed)
- Remove `index:chown_recurse()`
- Use `chown` command instead of `chown_recurse()`
- Add `-f` flag when using `rm -r` for the install dest directory

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
