# osxt

Unorthodox macOS command-line tools.

## Command-line Interface

### `osxiso` &mdash; Generate a macOS ISO image file.

  [0]: http://www.insanelymac.com/forum/topic/309654-run-vanilla-os-x-el-capitan-sierra-yosemite-or-mavericks-in-virtualbox-5010-on-a-windows-host/

Allows you to build a macOS ISO image file from an OSX installer application
like "Install macOS Sierra.app". *Based on [fusio71au@insanelymac.com][0]'s work.* 

### `xcode` &mdash; Download and install XCode Command-line Tools.

Allows you to download and install any XCode Command-line Tools. Check out
[`xcode/README.md`](xcode/README.md) for more information.

#### `download`

Download an XCode Command-line Tools Disk Image File.

#### `install`

Install XCode Command-line Tools from a Disk Image File.

#### `getpbzx`

  [pbzx]: https://github.com/NiklasRosenstein/pbzx

Download [pbzx], which is required for installing the XCode Command-line Tools
in Version 8.0 or newer.

#### `getversion`

Extract `clang` from a Disk Image File and print its version. *Note: Currently,
this unpacks the whole archive and is thus not actually more efficient than
using the `install` command and calling `clang -V` yourself.*
