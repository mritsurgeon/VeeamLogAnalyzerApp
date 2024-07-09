# Veeam Log Analyzer

## Overview
The Veeam Log Analyzer is a PyQt5-based application designed to analyze and visualize logs from Veeam software. It provides a user-friendly interface to load logs, filter them based on severity levels, display logs with syntax highlighting, visualize log events over time using Matplotlib, and search error descriptions online.

## Features
- **Load Logs**: Load multiple log files (.log) into the application.
- **Filter Logs**: Filter logs based on severity levels (Error, Warning, Info, View).
- **Display Logs**: Display filtered logs with syntax highlighting based on severity.
- **Show Timeline**: Visualize log events over time using a stacked bar graph.
- **Search Online**: Search error descriptions online using Google search.

### Log Merging
The application supports merging multiple log files into a single view, enabling comprehensive analysis across different log sources.

## Prerequisites
Before running the application, ensure you have the following dependencies installed:

```bash
pip install PyQt5 matplotlib
```
PyQt5: Python bindings for Qt5, used for building the GUI.
matplotlib: Python plotting library, used for visualizing log events over time.

### Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/mritsurgeon/VeeamLogAnalyzerApp.git
   cd veeam-log-analyzer
   ```
2. Install dependencies using pip:
   ```bash
   pip install PyQt5 matplotlib
   ```
3. Run the application:
   ```bash
   python LogAnalyzerApp.py
   ```
4. Use the interface to load log files, filter logs, view log details, and visualize log events over time.

### Screenshots

![image](https://github.com/mritsurgeon/VeeamLogAnalyzerApp/assets/59644778/05ddf55b-2979-46ef-a8c2-77e376a1351e)




![image](https://github.com/mritsurgeon/VeeamLogAnalyzerApp/assets/59644778/23b03a01-b4a9-43fb-bd02-f69083d8014c)

   
