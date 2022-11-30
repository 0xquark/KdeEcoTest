# KdeEcoTest | KdeEcoTestCreator

![KDE-ECO-TEST IMAGE](Kdeecotest.png)
`KdeEcoTest` and `KdeEcoTestCreator` are python based tools designed for reproducing computer actions by simulating keyboard and mouse acitivity.

Contents
========
* [Why?](#why)
* [Installation](#installation)
* [Usage](#usage)
* [Want to contribute?](#want-to-contribute)

### Why?
A Standard Usage Scenario reflects the typical functions of an application and is central to measuring the energy consumption of software.
`KdeEcoTestCreator` helps to create a script which simulates the task of a normal user do in order to create standard usage scenario.
`KdeEcoTest` runs the script created by KdeEcoTestCreator to automate the scenario and helps to measure energy consumption of that application.

KdeEcoTest and KdeEcoTestCreator is a cross-platform and CLI based python tool which is built using xdotool.

### Installation
> In order to run KdeEcoTestCreator and KdeEcoTest , These modules are required to be installed on your device.

```bash
$ pip3 install python-libxdo
$ pip3 install pynput
$ sudo apt-get install xdotool
```

### Usage

```bash
$ git clone https://invent.kde.org/teams/eco/feep.git
$ cd feep/tools/KdeEcoTest/
```

#### KdeEcoTestCreator usage

- To start KdeEcoTestCreator :
```bash
$ python3 KdeEcoTestCreator.py --outputFilename KdeEcoTestScript.txt
```
- A round mouse pointer appears , Click on the window you want to test.Now, You can use these options provided by KdeEcoTestCreator to simulate actions and create a test script.
```shell
Commands:
dw: define window.
ac: add clicks.
sc: stop add clicks.
ws: write to the screen.
wtl: write test timestamp to log.
wmtl: write message to log.
```

#### KdeEcoTest usage
KdeEcoTest automates the actions stored in the script created by KdeEcoTestCreator.
- To run KdeEcoTest script :
```bash
python3 KdeEcoTest.py --inputFilename KdeEcoTestScript.txt
```
- To pause the test : Press F1
- To abort the program : Press F2

### Want to contribute?
> Before contributing, fork the repository and make a MR when you fix the issue.

Contribute in the following ways:

#### To-Do's
- Negative value problem : There's a problem with negative values when script is created on another computer and played on a different computer.

- Improve Interactions : Find a way to quit Kdeecotest(using space or esc) more easily , this means justmake the tool more easier for everyone to use.

- Modal window : KDE-ECOTEST Doesn't record the clicks on modal window.We need to find a way to add it.

- Keyboard Activity : Curently kdeecotest only capture mouse activity with typing text as the only keyboard activity. We want to record keyboard controls too,Find a way to add keyboard activity.

- Documentation : You can always improve the documentation making it more easier forpeople to use this tool and contribute to it.

Ask Questions at : [KDE-Energy Efficency Matrix](https://matrix.to/#/#energy-efficiency:kde.org)
