# GNDU-Result-Compiler

![Debug Status](https://github.com/anhatsingh/GNDU-Result-Compiler/actions/workflows/python-package2.yml/badge.svg?branch=v3)
![Build Status](https://github.com/anhatsingh/GNDU-Result-Compiler/actions/workflows/python-package.yml/badge.svg?branch=v3)

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Downloads](https://img.shields.io/badge/download-all%20releases-brightgreen.svg)](https://github.com/anhatsingh/GNDU-Result-Compiler/releases/)

## About

This package uses the `Python requests Library` and `Selenium Library`
with **Google Sheets API v4** to compile marks of students of GNDU in Google Sheets.

## Changelog
Version 3.x
1. Implements `requests` library of python instead of `Selenium` library to get the results.
2. Uses `MultiThreading` and `Queuing` to increase the speed of getting the results.
3. Has a Time Reduction factor of 142.2 in comparison to Version 1.x
4. Has the option to upload to same sheet or a new Google Sheet.

Version 2.x
1. Implements `Selenium` library with the support of `MultiThreading` to get the results.
2. Has a better overall organisation of code in comparison to Version 1.x
3. Has a Time Reduction Factor of 4.1 in comparison to Version 1.x

Version 1.x
1. Implements `Selenium` library to get the Result of students Sequentially.
2. Compiles the data into a single Google Sheet.

The lead developer is Anhat Singh

## Building / Installing Python-Auto-Attendance

### Pre-Requisites
1. Install the Python dependencies by running the following pip commands
    ```
    pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib    
    ```
2. Use the included `chromedriver.exe` or download the latest one from [ChromeDriver - WebDriver for Chrome](https://chromedriver.chromium.org/) and keep it in the root directory.
3. Follow bullet 3 and 4 of Prerequisites at [Google Sheets API v4 Guide](https://developers.google.com/sheets/api/quickstart/python) to create a Google Cloud Platform Project, enable Sheets API and get the Google `credentials.json` file to be put into the root directory.

## Running Python-Auto-Attendance

* Simple run the following command:
    ```
    py app.py
    ```
### How to Use
After following all the steps given in Pre-requisites, open `app.py`, change the variables given according to your needs.

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
