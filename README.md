## **Diskttoritor - Disk-Space-Monitor-linux**

A Python script to monitor disk space and perform automatic backups.

**Description**

This script uses the `psutil` library to monitor the disk space of the directories specified in the configuration file. When the disk space exceeds the configured threshold, the script displays an alert and performs a backup of the specified directories.

**Features**

* Real-time disk space monitoring
* Customizable alerts with title and message
* Automatic backups of specified directories
* Configurable through a JSON file
* Support for multiple languages

**Requirements**

* Python 3.6 or later
* `psutil` library (can be installed with `pip install psutil`)
* `json` library (included in Python)

**Installation**

1. Clone the repository with `git clone https://github.com/Rip70022/Disk-Space-Monitor-linux.git`
2. Install dependencies with `pip install -r requirements.txt`
3. Edit the `config.json` file to configure the script according to your needs
4. Run the script with `python diskttoritor.py`

**Configuration**

The `config.json` file contains the following configuration options:

* `language`: script language (default: English)
* `disk_paths`: list of directories to monitor
* `threshold_percent`: disk space threshold to display alert (default: 90%)
* `check_interval`: time interval between disk space checks (default: 5 minutes)
* `alert_color`: alert color (default: red)
* `backup`: backup configuration (default: disabled)

**Usage**

1. Edit the `config.json` file to configure the script according to your needs
2. Run the script with `sudo python diskttoritor.py`
3. The script will monitor disk space and display alerts and perform backups according to the configuration

**License**

This script is licensed under the MIT License.
