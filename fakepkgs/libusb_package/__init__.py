import ctypes
import os
import usb.backend.libusb1 as libusb1

_LIBUSB_PATH = "/data/data/com.termux/files/usr/lib/libusb-1.0.so"
_backend = None


class _FakeDeviceHandle:
    """Mimics usb.backend.libusb1._DeviceHandle but skips libusb_open — we already
    have an open handle from libusb_wrap_sys_device."""
    def __init__(self, devid, handle):
        self.devid = devid
        self.handle = handle


def get_libusb1_backend():
    global _backend
    if _backend is not None:
        return _backend

    lib = libusb1._load_library(find_library=lambda x: _LIBUSB_PATH)
    libusb1._setup_prototypes(lib)

    lib.libusb_set_option.restype = ctypes.c_int
    lib.libusb_set_option(None, 2)  # NO_DEVICE_DISCOVERY

    backend_obj = libusb1._LibUSB(lib)
    libusb1._lib = lib
    libusb1._lib_object = backend_obj

    fd_str = os.environ.get("TERMUX_USB_FD")
    if fd_str:
        fd = int(fd_str)
        lib.libusb_wrap_sys_device.argtypes = [
            ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(ctypes.c_void_p)
        ]
        lib.libusb_wrap_sys_device.restype = ctypes.c_int
        lib.libusb_get_device.argtypes = [ctypes.c_void_p]
        lib.libusb_get_device.restype = ctypes.c_void_p

        real_handle = ctypes.c_void_p()
        r = lib.libusb_wrap_sys_device(backend_obj.ctx, fd, ctypes.byref(real_handle))
        if r == 0:
            dev_ptr = lib.libusb_get_device(real_handle)
            wrapped_dev = libusb1._Device(dev_ptr)

            def _enumerate_override():
                yield wrapped_dev
            backend_obj.enumerate_devices = _enumerate_override

            def _open_device_override(dev):
                if dev is wrapped_dev:
                    return _FakeDeviceHandle(wrapped_dev.devid, real_handle)
                return libusb1._DeviceHandle(dev)
            backend_obj.open_device = _open_device_override

    _backend = backend_obj
    return _backend
