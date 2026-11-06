#!/data/data/com.termux/files/usr/bin/bash
set -e

echo "== Termux paketleri kuruluyor =="
pkg update -y
pkg install -y python git libusb termux-api

echo "== wifit3 klonlanıyor =="
if [ ! -d "$HOME/wifit3" ]; then
    git clone https://github.com/rehimlianar/wifit3.git "$HOME/wifit3"
fi

echo "== Python bağımlılıkları kuruluyor =="
pip install platformdirs pyusb rich textual

echo "== Sahte libusb_package kopyalanıyor =="
mkdir -p "$HOME/fakepkgs/libusb_package"
cp "$(dirname "$0")/fakepkgs/libusb_package/__init__.py" "$HOME/fakepkgs/libusb_package/"

echo "== Sarmalayıcı script kopyalanıyor =="
cp "$(dirname "$0")/run_wifit3.py" "$HOME/wifit3/"

echo "== Launcher kuruluyor =="
mkdir -p "$HOME/bin"
cp "$(dirname "$0")/wifit3-run" "$HOME/bin/"
chmod +x "$HOME/bin/wifit3-run"

if ! grep -q 'HOME/bin' "$HOME/.bashrc" 2>/dev/null; then
    echo 'export PATH="$HOME/bin:$PATH"' >> "$HOME/.bashrc"
fi

source "$HOME/.bashrc"

echo "== Tamamlandı. 'wifit3-run' yazarak çalıştırabilirsin. =="
echo "== NOT: Termux:API Android uygulamasını (Play Store/F-Droid) ayrıca kurman ve USB izni vermen gerekiyor. =="
