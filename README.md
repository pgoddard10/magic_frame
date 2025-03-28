# Magic Frame

## Hardware

### Witty Pi 4 L3V7

If not using as a hat, the following pins need connecting to the Pi:
5v, GPIO2 (SDA I2C), GPIO3 (SLC I2C), GPIO4, Ground, GPIO5, GPIO6. These are pin numbers 2, 3, 5, 7, 9, 29, and 31 respectively. Some alternatives are possible, e.g. there are multiple pins for Ground.

Witty Pi user manual: https://www.uugear.com/doc/WittyPi4L3V7_UserManual.pdf

### WaveShare 7.3inch ACeP 7-Color E-Paper E-Ink Display Module 800x480
Set up pins/connections as per https://www.waveshare.com/wiki/7.3inch_e-Paper_HAT_(F)_Manual#Hardware_Connection
Install the Python software as per https://www.waveshare.com/wiki/7.3inch_e-Paper_HAT_(F)_Manual#Python

Full user manual: https://www.waveshare.com/wiki/7.3inch_e-Paper_HAT_(F)_Manual

## Initial Setup
1. Enable i2c and SPI in the raspi-config
2. Install the requirements.txt
3. Install the WittyPi software (see their manual)
4. Install the WaveShare software (see their manual). It is important to `make` the WaveShare software to generate the `.so` files needed for the drivers in the next step.
5. Copy the WaveShare drivers from their demo into `src/epaper/drivers` (replace the existing files in this folder) https://github.com/waveshareteam/e-Paper/tree/master/RaspberryPi_JetsonNano/python/lib/waveshare_epd - specifically, the epd7in3e.py, epd7in3f.py, epd7in3g.py, epdconfig.py, sysfs_gpio.so, sysfs_software_spi.so, and the __init__.py files.
5. Back in the magic_frame folder, run `sudo chmod +x install.sh`
6. `./install.sh`

## Configuring remote config

Since Magic Frame is turned off most of the time, we can't really log into it. But we can set up a remote server and a shared folder, put our config in there and point Magic Frame to it.
This assumes you already have a working server with an NFS shared folder on your local network.

1. SSH into Magic Frame and run:
`sudo nano /etc/fstab `

1. Add this to the file you just opened:
`192.168.1.33:/vault /var/vault nfs rw,soft,intr,rsize=8192,wsize=8192,timeo=5 0 0`

2. `sudo nano /etc/systemd/system/vault.service`

3. Paste this into the newly created file:
```ini
[Unit]
Description = Vault NFS mount.
After = network.target, multi-user.target
Before = magic_frame.service

[Service]
WorkingDirectory=/home/
ExecStart = sudo mount /var/vault

[Install]
WantedBy = multi-user.target
```
For this example, we assume that our server has local ip of `192.168.1.33` and has a shared NFS directory named `vault`.

3. `sudo systemctl daemon-reload`
4. `sudo systemctl enable vault.service`
5. `sudo systemctl start vault.service`
6. Now if we do `ls /var/vault`, we'll see the contents of the shared directoy. It can be used
7. Go to `src/config.json` and change `remote_config` field to be `/var/vault/path/to/your/config.json`
