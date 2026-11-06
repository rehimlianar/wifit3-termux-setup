import os
import sys

# termux-usb -e appends the fd as the LAST argv item. Pop it off before
# wifit3's own arg parser ever sees it.
if len(sys.argv) > 1 and sys.argv[-1].isdigit():
    os.environ["TERMUX_USB_FD"] = sys.argv.pop()

from wifit3.__main__ import main
main()
