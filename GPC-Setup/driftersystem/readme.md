
use rc.local

Edit the rc.local File:
Open the /etc/rc.local file in an editor (you might need to create it if it doesn't exist).
Add the command to start your script before the exit 0 line:

/usr/bin/python3 /path/to/your_script.py &
Make sure the script is executable:
bash
Copy code
chmod +x /path/to/your_script.py
Enable rc.local for Execution:
Ensure that rc.local is executable:
bash
Copy code
sudo chmod +x /etc/rc.local
If your system uses systemd, you might need to ensure the rc-local service is enabled:
Copy code
sudo systemctl enable rc-local


Please install gpiod

sudo apt update
sudo apt install python3-libgpiod
