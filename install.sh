#!/bin/sh

git submodule init
git submodule update

if [ ! -z $(which apt) ]; then
  apt install -y curl mailutils || exit 1
elif [ ! -z $(which yum) ]; then
  yum install -y curl mailx || exit 1
fi

cd watchdog
./uninstall.sh
./install.sh
cd - > /dev/null

if [ -f /usr/local/bin/gan-watchdog.py ] || [ -f /lib/systemd/system/gan-watchdog@.service ]; then
  echo "Already installed, please uninstall first to reinstall!"
  exit 1
fi

cp -n gan-watchdog.py /usr/local/bin/
cp -n gan-watchdog@.service /lib/systemd/system/

mkdir -p /etc/gan-watchdog

if [ ! -f /etc/gan-watchdog/example.toml ]; then
  cp -n example.toml /etc/gan-watchdog
fi

systemctl daemon-reload
