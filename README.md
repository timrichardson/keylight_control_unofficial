# keylight_control_unofficial

command line tool for Elgato Keylight

There can potentially be more than one of these, but I only have one, and this command is hardcoded to use the first one it finds. 

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

  `keylight-control --bright 50`

  Credit to https://github.com/adamesch/elgato-key-light-api for work done in documenting the REST-style API.