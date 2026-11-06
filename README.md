# wifit3 Termux Without Root

Setup for running [wifit3](https://github.com/derv82/wifit3) on rootless Termux with adapters like the RTL8812AU.

Huge thanks to [derv82](https://github.com/derv82) for creating wifit3, the actual tool this setup wraps.

## How it works

wifit3 talks to the wireless adapter directly over USB (via PyUSB/libusb), without needing a rooted device or kernel-level monitor mode. On Android this means going through `termux-usb`, which hands off an open file descriptor instead of a `/dev/bus/usb/...` path.

This setup bridges that gap:
- `install.sh` installs the required packages, clones wifit3, and wires everything together.
- A fake `libusb_package` backend (`fakepkgs/libusb_package`) wraps libusb's `libusb_wrap_sys_device` so it can use the file descriptor Android hands over, instead of trying to open the device itself.
- `run_wifit3.py` strips the file descriptor argument that `termux-usb -e` appends and passes it to wifit3 via an environment variable.
- `wifit3-run` ties it together: finds the adapter with `termux-usb -l`, requests access, and launches wifit3 with the right `PYTHONPATH`.

## Requirements

- [Termux](https://termux.dev/) (F-Droid build recommended)
- [Termux:API](https://github.com/termux/termux-api) — both the Termux package **and** its companion Android app, from the **same source** (F-Droid or Play Store, not mixed)
- A [supported USB Wi-Fi adapter](https://github.com/derv82/wifit3#supported-hardware) (e.g. RTL8812AU)
- A USB-OTG cable/adapter, and a device whose USB-C port supports host mode
- Android with OTG/host mode working — on some custom ROMs (e.g. LineageOS) this may need a reboot after flashing before USB host mode starts working correctly

## Installation
```bash
git clone https://github.com/rehimlianar/wifit3-termux-without-root.git ~/wifit3-termux-without-root
cd ~/wifit3-termux-without-root
bash install.sh
source ~/.bashrc
```

## Usage
```bash
wifit3-run
```

## Troubleshooting

**`wifit3-run: command not found`**
Run `source ~/.bashrc` (or open a new Termux session) so the `~/bin` launcher directory is picked up.

**`termux-usb: command not found`**
Install the Termux:API package: `pkg install termux-api`. Make sure the Termux:API Android app is also installed.

**`USB cihazı bulunamadı` / "USB device not found" (`termux-usb -l` returns `[]`)**
- Confirm the adapter is plugged in through a working OTG cable/adapter.
- Check that your device's USB-C port actually supports host (OTG) mode.
- On some ROMs, USB host mode only activates after a reboot — try rebooting with the adapter connected.
- Make sure the Termux:API app has been granted permission when prompted.

## Uninstalling

```bash
rm -rf ~/wifit3-termux-without-root
rm -rf ~/wifit3
rm -rf ~/fakepkgs
rm -f ~/bin/wifit3-run
pip uninstall -y platformdirs pyusb rich textual
```

## License

This setup script is provided as-is. wifit3 itself is licensed under [GPL-2.0](https://github.com/derv82/wifit3/blob/master/LICENSE) — see the upstream repository for details.
