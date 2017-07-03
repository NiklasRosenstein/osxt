# Copyright (c) 2017  Niklas Rosenstein
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import click
import os
import sys
import {main} from './main'
import system from  '../xcode/system'

# From http://www.insanelymac.com/forum/topic/309654-run-vanilla-os-x-el-capitan-sierra-yosemite-or-mavericks-in-virtualbox-5010-on-a-windows-host/
DEVICE_SERIALS = {
  'iMac11,3': 'Mac-F2238BAE',
  'MacBookPro11,3': 'Mac-2BD1B31983FE1663',
  'MacMini6,2': 'Mac-F65AE981FFA204ED'
}
CPU_IDS = {
  'Lynnfield-i5-750': '00000001 000106e5 06100800 0098e3fd bfebfbff',
  'IvyBridge-0': '00000001 000306a9 04100800 7fbae3ff bfebfbff',
  'IvyBridge-1': '00000001 000306a9 00020800 80000201 178bfbff'
}


def vbcall(prog, *args, **kwargs):
  if os.name == 'nt' and not os.path.isabs(prog):
    prog = os.path.join('C:\\Program Files\\Oracle\\VirtualBox', prog)
  return system.call(prog, *args, **kwargs)


def manage(*args, **kwargs):
  return vbcall('VBoxManage', *args, **kwargs)


@main.command()
@click.argument('vm')
@click.option('--new', is_flag=True, help='Create a new VM. Implies --all')
@click.option('--all', is_flag=True, help='Do all configuration settings.')
@click.option('--storage', is_flag=True, help='Set up storage configuration.')
@click.option('--image', help='Disk image to attach. Only with --storage.')
@click.option('--general', help='General settings such as memory, vram, cpu count, firmware, etc.')
@click.option('--device', help='Configure a specific host device. If --all '
    'is used, the default device is MacBookPro11,3.')
@click.option('--device-serial', help='Manually specify the device serial number. '
    'Must be paired with a --device name.')
@click.option('--cpu', help='CPU ID set. Not implied with --all, but implied '
    'by --new with a default value of "IvyBridge-0". Must be one of the '
    'available CPU ID set names or a string formatted as a CPU ID set (5 '
    '64-bit hex numbers).')
@click.option('--resolution', help='Set the display resolution. Must be an '
    'integer between 0 and including 5, referring to 640x480, 800x600, '
    '1024x768, 1280x1024, 1440x900 and 1920x1200 respectively. If --new is '
    'used, a default value of 4 is used (1440x900).')
def osxvbm(vm, new, all, storage, image, general, device, device_serial, cpu, resolution):
  if device and device not in device_serials and not device_serial:
    print('error: unknown device: {!r}')
    print('error: add --device-serial to manually specify the serial number')
    sys.exit(1)
  if device_serial and not device:
    print('error: missing --device option with --device-serial is specified')
    sys.exit(1)
  if new and not cpu:
    cpu = 'IvyBridge-0'
  if cpu:
    parts = cpu.split(' ')
    if len(parts) != 5 or not all(len(x) == 8 for x in parts):
      if cpu not in CPU_IDS:
        print('error: invalid CPU ID: {!r}'.format(cpu))
        sys.exit(1)
      cpu = CPU_IDS[cpu]
  if resolution and resolution not in ('0', '1', '2', '3', '4', '5'):
    print('error: invalid resolution: {!r}'.format(resolution))
    sys.exit(1)
  if new and not resolution:
    resolution = '4'

  if new:
    all = True
    manage('createvm', '--name', vm, '--ostype', 'MacOS_64', '--register')
  if storage or all:
    manage('storagectl', vm, '--name', 'SATA Controller', '--add', 'sata', '--controller', 'IntelAHCI')
    if image:
      manage('storageattach', vm, '--storagectl', 'SATA Controller', '--port',
        '0', '--device', '0', '--type', 'hdd', '--medium', os.path.abspath(image))
  elif image:
    print('warning: --image only with --storage')
  if general or all:
    options = (
      '--audiocontroller hda '
      '--chipset ich9 '
      '--firmware efi '
      '--cpus 2 '
      '--hpet on '
      '--keyboard usb '
      '--memory 4096 '
      '--mouse usbtablet '
      '--vram 128 '
    ).split()
    manage('modifyvm', vm, *options)
  if cpu:
    manage('modifyvm', vm, '--cpuidset', *cpu.split(' '))
  if device or all:
    if not device:
      device = 'MacBookPro11,3'
    if not device_serial:
      device_serial = DEVICE_SERIALS[device]
    manage('setextradata', vm, 'VBoxInternal/Devices/efi/0/Config/DmiSystemProduct', device)
    manage('setextradata', vm, 'VBoxInternal/Devices/efi/0/Config/DmiSystemVersion', '1.0')
    manage('setextradata', vm, 'VBoxInternal/Devices/efi/0/Config/DmiBoardProduct', device_serial)
    manage('setextradata', vm, 'VBoxInternal/Devices/smc/0/Config/DeviceKey',
      'ourhardworkbythesewordsguardedpleasedontsteal(c)AppleComputerInc')
    manage('setextradata', vm, 'VBoxInternal/Devices/smc/0/Config/GetKeyFromRealSMC', '1')
  if resolution:
    manage('setextradata', vm, 'VBoxInternal2/EfiGopMode', resolution)


@main.command(context_settings={'ignore_unknown_options': True})
@click.argument('args', nargs=-1)
def vbm(args):
  " Shorthand for VBoxManage. Useful on Windows. "

  manage(*args)
