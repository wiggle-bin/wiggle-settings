# WiggleSettings

## Via CLI

Run `wiggle-settings` to listen to the setting.json file. Any updates in the json file will be reflected on the WiggleBin.

```
wiggle-settings
```

## Install WiggleSettings service

In the terminal run `wiggle-settings-install`. This will install and start a service which runs `wiggle-settings` on boot.

```
wiggle-settings-install
```


You can check the status with:

```
systemctl --user status wiggle-settings.service
```

To stop the service run:

```
systemctl --user stop wiggle-settings.service
```

To start the service run:

```
systemctl --user start wiggle-settings.service
```

## Installation for development

Updating packages on Raspberry Pi
```
pip install --upgrade pip setuptools wheel
python -m pip install --upgrade pip
apt-get install libjpeg-dev zlib1g-dev
```

Installing package
```
pip3 install -e .
```

For installation without dev dependencies
```
pip install --no-dev -r requirements.txt
```