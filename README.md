# keylight_control_unofficial

command line tool for Elgato

```
    usage: keylight_control [-h] [--bright BRIGHT] [--temp TEMP] [--ip IP]

    Sets brightness and color temperature of an Elgato keylight. It assumes there is only one such light. ip of auto will attempt to find the IP address of the lamp.

    options:
      -h, --help       show this help message and exit
      --bright BRIGHT  set brightness, 0 to 100. O will turn lamp off
      --temp TEMP      set color K. Range is 2900K to 7000K
      --ip IP          Use auto to find it with avahi aka zeroconf.
```

  This is published on the snap store, where the command looks like this:

  `keylight-cli-unofficial.keylight-control --bright=50`