#!/bin/python3 -B

import watchdog
import sys
import toml

def main():
  if len(sys.argv) != 2:
    print('[ERROR   ] Wrong numbers of parameters. Usage: {} <config.toml>'
        .format(sys.argv[0]))
    exit(1)

  config = toml.loads(open(sys.argv[1], 'r').read())

  def get_config(*name, **kwargs):
    c = config

    for n in name:
      if n in c:
        c = c[n]
      else:
        if 'default' in kwargs:
          return kwargs['default']
        else:
          raise ValueError('configure field "{}" not present'.format('.'.join(name))) 

    return c

  shadowsocks = get_config('config', 'shadowsocks')
  wireguard = get_config('config', 'wireguard')

  sender = get_config('email', 'sender')
  receiver = get_config('email', 'receiver')

  probe = get_config('check', 'probe')
  tries = get_config('check', 'tries', default=3)
  timeout = get_config('check', 'timeout', default=5)
  interval = get_config('check', 'interval', default=60)

  watchdog.watchdog({
    'check': {
      'cmd': 'ping -c {} -t {} {}'.format(tries, timeout, probe),
      'interval': interval},
    'rise': [{
      'cmd': 'ip addr | mailx -s "[$(uname -n)] GAN Reconnected" -r "{} ($(uname -n))" {}'.format(sender, receiver)}],
    'low': [
        {'cmd': 'systemctl restart shadowsocks-libev-tunnel@{}.service'.format(shadowsocks)},
        {'cmd': 'systemctl restart wg-quick@{}.service'.format(wireguard)}]})

if __name__ == '__main__':
  watchdog.app(main)
