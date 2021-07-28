# Google-Meet-Automator

![Debug Status](https://github.com/anhatsingh/Google-Meet-Automator/actions/workflows/python-package.yml/badge.svg?branch=v3)
![Build Status](https://github.com/anhatsingh/Google-Meet-Automator/actions/workflows/python-app.yml/badge.svg?branch=v3)

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Downloads](https://img.shields.io/badge/download-all%20releases-brightgreen.svg)](https://github.com/anhatsingh/Google-Meet-Automator/releases/)

## About

This application uses the `Selenium` Library with `Whatsapp Python API`
with **Google Meets** Integration and **OBS Record Support** to automatically join Google Meeting, Start Recording, Wait for Participants to reduce to minimum number, exit Meeting, end recording, all while giving the status through Whatsapp using `Whatsapp Python API`.

## Changelog
Version 3.x
1. Implements `Whatsapp Python API` to get messages and report back to user using a single group.
2. Has additional interactive functionality to interact with the user using whatsapp bot.

Version 2.x
1. Implements `Selenium` library with the support of `MultiThreading` to implement the Automation.
2. Is entirely written again from scratch.
3. Has multiple support libraries updated for better functionality
4. Uses Databases to better track the messages it has seen.
5. Implements YAML standarization to store constants for easy access.

Version 1.x
1. Implements `Selenium` library to Join Meetings by getting links through multiple groups.
2. Start OBS recording automatically
3. End Recording automatically.

The lead developer is Anhat Singh

## Building / Installing Google-Meet-Automator

### Pre-Requisites
1. Install the Python dependencies by running the following pip commands
    ```
    pip install -r requirements.txt --no-index --find-links file:///tmp/packages    
    ```
2. Use the included `chromedriver.exe` or download the latest one from [ChromeDriver - WebDriver for Chrome](https://chromedriver.chromium.org/) and keep it in the root directory.

## Running Google-Meet-Automator

* Simple run the following command:
    ```
    py app.py
    ```
### How to Use
After following all the steps given in Pre-requisites, open `config.yml`, change the constants given according to your needs.
More coming soon.

## License

    The code in this repository is licensed under the GNU General Public Licence, Version 3.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       https://www.gnu.org/licenses/gpl-3.0.en.html

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

**NOTE**: This software depends on other packages that may be licensed under different open source licenses.
