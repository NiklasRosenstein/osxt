# osxt

Unorthodox macOS command-line tools.

## Command-line Interface

  [0]: http://www.insanelymac.com/forum/topic/309654-run-vanilla-os-x-el-capitan-sierra-yosemite-or-mavericks-in-virtualbox-5010-on-a-windows-host/

<p><details>
  <summary><code>osxiso</code> &mdash; Generate a macOS ISO image file.</summary>

  Allows you to build a macOS ISO image file from an OSX installer application
  like "Install macOS Sierra.app". *Based on [fusio71au@insanelymac.com][0]'s work.* 
</details></p>

<p><details>
  <summary><code>osxvbm</code> &mdash; Create and/or configure a VirtualBox VM for macOS</summary>

  Configure a VirtualBox virtual machine for macOS. Can also create a new
  machine and immediately configure it. Setting up a new macOS virtual machine
  has never been easier (works on all host systems).

  1. Run `$ oxst osxvbm "macOS El Capitan" --new`
  2. Go to the machine's Storage settings
  3. Add a new Virtual Hard Disk 
  3. Add a new Optical Drive pointing to your macOS ISO

  You can generate a new ISO image for macOS using the `osxt osxiso` command
  on an actual Mac.

</details></p>

<p><details>
  <summary><code>xcode</code> &mdash; Download and install XCode Command-line Tools.</summary>

  Allows you to download and install any XCode Command-line Tools. Check out
  <a href="xcode/README.md"><code>xcode/README.md</code></a> for more
  information.

  <details>
    <summary><code>&nbsp; download</code></summary>
    <p>
    Download an XCode Command-line Tools Disk Image File.
    </p>
  </details>

  <details>
    <summary><code>&nbsp; install</code></summary>
    <p>
    Install XCode Command-line Tools from a Disk Image File.
    </p>
  </details>

  <details>
    <summary><code>&nbsp; getpbzx</code></summary>
    <p>
    Download <a href="https://github.com/NiklasRosenstein/pbzx">pbzx</a>,
    which is required for installing the XCode Command-line Tools in
    Version 8.0 or newer.
    </p>
  </details>

  <details>
    <summary><code>&nbsp; getversion</code></summary>
    <p>
    Extract <code>clang</code> from a Disk Image File and print its version.
    <em>Note: Currently, this unpacks the whole archive and is thus not
    actually more efficient than using the <code>install</code> command and
    calling <code>clang -V</code> yourself.</em>
  </details>

</details></p>
