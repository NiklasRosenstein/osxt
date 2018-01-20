# osxt

> `usage: osxt.exe [-h] {mkiso,vbx,vbm,xcode,getpbzx} ...`

### XCode Version Table

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
