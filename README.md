# RPiCigaDetector

## Overview

This project is to detect and count the cigarette butts and save the information with the time stamp into the Mysql database
on Raspberry Pi.
The custom model to detect the cigarette butts is trained - ssd_mobilenet_v2 and is converted into tflite model to speed up
the detection processing by USB Coral Accelerator. The frame rate is 50 fps.
The GUI of this project is designed with Kivy.

## Structure

- gui

    The Kivy files and source code for GUI

- src

    The main source code to detect and count the cigarette butts on Raspberry Pi
    
- utils

    * The models for cigarette butts detection
    * The source code for utilities of the project
    
- app

    The main execution file
    
- pi_requirements

    All the dependencies on Raspberry Pi

- requirements

    All the dependencies for PC

- settings

    Several settings including database configuration

## Installation

- Environment

    Ubuntu 18.04/Raspbian OS, Python 3.6

- Installation on Raspberry Pi

    * Please run the following commands in the terminal

        ```
            sudo apt-get update
            sudo apt-get dist-upgrade
        ```
    * While we're at it, let's make sure the camera interface is enabled in the Raspberry Pi Configuration menu. 
    Please click the Pi icon in the top left corner of the screen, select Preferences -> Raspberry Pi Configuration, 
    and go to the Interfaces tab and verify Camera is set to Enabled. If it isn't, enable it now, and reboot the Raspberry Pi.
    
    * Please run the following commands in the terminal.
    
    ```
        sudo apt-get install -y git
        git clone https://github.com/evg-cv/RPiCigDetector.git
        cd RPiCigDetector        
        bash pi_requirements.sh        
    ```
    
- Database Configuration on Raspberry Pi

    * Please run the following command to begin the MySQL securing process.
    ```
        sudo mysql_secure_installation         
    ```
  
    * Just follow the prompts to set a password for the root user and to secure your MySQL installation. 
    For a more secure installation, you should answer “Y” to all prompts when asked to answer “Y” or “N“.
    * Now please access your Raspberry Pi’s MySQL server and create your database called "butt_counter" by entering the 
    following commands.
    ```
        sudo mysql -u root -p
        CREATE DATABASE butt_counter;
        ALTER USER 'root'@'localhost' IDENTIFIED BY 'password';
        exit
    ```

- Installation on PC

    Please navigate to this project directory and run the following command in the terminal.
    
    ```
        pip3 install -r requirements.txt
        sudo apt-get install libedgetpu1-std
        pip3 install --extra-index-url https://google-coral.github.io/py-repo/ tflite_runtime
        sudo apt-get install xclip
    ```

- Please install Mysql database on Ubuntu 18.04 and create database called "butt_counter".

## Execution

- Please connect USB Coral Accelerator with your PC/Raspberry Pi 4 via USB 3.0 port and web camera with PC/Raspberry Pi.

- Please navigate to this project directory and run the following command in the terminal.

    ```
        python3 app.py
    ```
