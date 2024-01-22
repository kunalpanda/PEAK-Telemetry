# PEAK-Telemetry

## Project Overview
PEAK-Telemetry is a Python-based project that creates a GUI for displaying battery voltages over a CAN (Controller Area Network). It is currently being developed to include a DBC file for defining IDs and data types for display.

- `test.py`: Contains the stable application.
- `projectrequirementdocumenttemplate.pdf`: Outlines the software's uses and priorities.
- `PCANBasic.py`: A local copy of the PCAN library.
- `fullapp.py`: Under development project to dynamically filter messages based on the CAN database file.

## Technical Details
- Python Version: Compatible with all versions of Python 3.
- Libraries:
  - `PCANBasic`: [Download from PEAK-System](https://www.peak-system.com/PCAN-XCP-API.445.0.html?&L=1)
  - `Matplotlib`: Install via `pip install matplotlib`
  - `Tkinter`: Install via `pip install tk`
  - `Python-Can` and `Cantools`: Install via `pip install python-can` and `pip install cantools`

## Installation
Ensure to install the necessary drivers and libraries as mentioned above.

## Usage
Run `test.py` to launch the application. The current version works without a DBC file and has a hardcoded message ID filter.

## Branch Details
This branch is stable and demonstrates proof of concept without the use of a DBC file.

## Note
This repository is currently not open for collaborations.
