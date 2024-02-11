import os
from pathlib import Path


def install():
    scriptFile = Path(__file__).parent / f"service/wiggle-settings-boot.sh"
    serviceFile = Path(__file__).parent / f"service/wiggle-settings-service"
    os.system(f"sudo cp {scriptFile} /usr/bin/wiggle-settings-boot.sh")
    os.system(f"sudo cp {serviceFile} /etc/systemd/user/wiggle-settings-service")
    os.system("systemctl --user enable wiggle-settings-service")
    os.system("systemctl --user start wiggle-settings-service")
