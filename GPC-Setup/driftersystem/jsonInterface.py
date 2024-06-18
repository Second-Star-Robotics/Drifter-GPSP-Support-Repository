#Set of functions that loads a json file into memory

# Path: loadConfiguration.py
import json
import SerialInterface as dserial
import gpiod
import time
import os
import serial
import downloadDepthLog
import time

#define GPIOs
CONFIG_FLAG = 19  # Input GPIO to determine if charge cable present (if present set to jsonInterface.py else sensorCapture.py)
IDLE_FLAG = 20  # Output to indicate if the drifter is idle


# Global configuration dictionary
global_config = {
    "status": {
        "batteryVoltage": 0.0,
        "depth": 0.0,
        "temperature": 0.0,
        "pitch": 0,
        "roll": 0,
        "pumpSpeed": 0,
        "volumeDisplaced": 0,
        "internalVolume": 0,
        "totalsamples": 0,
        "samplesdownloaded": 0
    },
    "commands": {
        "pumpAction": "out",
        "tareVolume": True,
        "applySettings": False,
        "fetchSettings": False
    },
    "flags": {
        "NewMessageGUI": True,
        "NewMessageDrifter": False,
        "DrifterIdle": True,
        "Shutdown": False
    }
}

#Global pump power state
pumpPower = True

#Configure serial port using hard coded values and pass serial object (tty2)
def configureControlSerialPort():
    #Configurate Commport
    Commport = '/dev/ttyS2'
    baudrate = 57600
    timeout = 0.5
    stopbits = 1
    bytesize = 8
    parity = 'N'
    xonxoff = False
    flowcontrol = False

    ser = serial.Serial(Commport, baudrate, timeout=timeout, stopbits=stopbits, bytesize=bytesize, parity=parity, xonxoff=xonxoff, rtscts=flowcontrol, dsrdtr=flowcontrol)

    return ser

#Configure serial port using hard coded values and pass serial object for debugging (tty3)
def configureDebugSerialPort():
    #Configurate Commport
    Commport = '/dev/ttyS3'
    baudrate = 57600
    timeout = 0.5
    stopbits = 1
    bytesize = 8
    parity = 'N'
    xonxoff = False
    flowcontrol = False

    ser = serial.Serial(Commport, baudrate, timeout=timeout, stopbits=stopbits, bytesize=bytesize, parity=parity, xonxoff=xonxoff, rtscts=flowcontrol, dsrdtr=flowcontrol)

    return ser

#Load json file into memory
def load_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data
    
#Write json file to disk
def write_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    
#Get data by resgisterAddress
def returnByRegisterAddress(data, registerAddress):
    for entry in data['configurations']:  # assuming 'configurations' is the key in your JSON
        if entry['registerAddress'] == registerAddress:
            return entry
    return None  # If no matching entry is found

#Return value by registerAddress
def returnByRegisterAddress(data, registerAddress):
    for entry in data['configurations']:  # assuming 'configurations' is the key in your JSON
        if entry['registerAddress'] == registerAddress:
            return entry['value']
    return None  # If no matching entry is found

#Return registerName by registerAddress
def returnByRegisterAddress(data, registerAddress):
    for entry in data['configurations']:  # assuming 'configurations' is the key in your JSON
        if entry['registerAddress'] == registerAddress:
            return entry['registerName']
    return None  # If no matching entry is found

#return dataType by registerAddress
def returnByRegisterAddress(data, registerAddress):
    for entry in data['configurations']:  # assuming 'configurations' is the key in your JSON
        if entry['registerAddress'] == registerAddress:
            return entry['dataType']
    return None  # If no matching entry is found

#return value in correct datatype by Address
def returnByRegisterAddress(data, registerAddress):
    for entry in data['configurations']:  # assuming 'configurations' is the key in your JSON
        if entry['registerAddress'] == registerAddress:
            if entry['dataType'] == 'integer':
                return int(entry['value'])
            elif entry['dataType'] == 'float':
                return float(entry['value'])
            elif entry['dataType'] == 'string':
                return entry['value']
    return None  # If no matching entry is found

#Read configuration data from Drifter
def fetchSettings(ser, data):
    for entry in data['configurations']:
        registerAddress = int(entry['registerAddress'])
        registerName = entry['registerName']
        dataType = entry['dataType']

        #Read Value from register via serial read
        if dataType == 'integer':
            value = dserial.readRegisterInt(ser, registerAddress)
        elif dataType == 'float':
            value = dserial.readRegisterFloat(ser, registerAddress)
        elif dataType == 'string':
            value = dserial.readHeader(ser)

        #Update dictionary with new value
        entry['value'] = value

        print(f"{registerAddress}: {registerName} = {value}")

#Write configuration data to Drifter
def applySettings(ser, data):
    for entry in data['configurations']:
        registerAddress = int(entry['registerAddress'])
        registerName = entry['registerName']
        value = returnByRegisterAddress(data, registerAddress)
        print(f"{registerAddress}: {registerName} = {value}")

        #Write Value to register via serial write
        if entry['dataType'] == 'integer':
            dserial.writeRegisterInt(ser, registerAddress, value)
        elif entry['dataType'] == 'float':
            dserial.writeRegisterFloat(ser, registerAddress, value)
        elif entry['dataType'] == 'string':
            dserial.writeHeader(ser, value)

#Configurator.json interface functions

def pushStatus(file_path):
    """Update the JSON file with the current status from the global dictionary."""
    with open(file_path, 'r+') as file:
        data = json.load(file)
        data['status'] = global_config['status']
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()
        #close file
        file.close()
        print("Status updated in JSON file.")

def pullFlags(file_path):
    """Load the flags from the JSON file and update the global dictionary."""
    with open(file_path, 'r') as file:
        data = json.load(file)
        global_config['flags'] = data['flags']
        #close file
        file.close()
        print("Flags pulled from JSON file and updated in global dictionary.")

def pushFlags(file_path):
    """Update the JSON file with the current flags from the global dictionary."""
    with open(file_path, 'r+') as file:
        data = json.load(file)
        data['flags'] = global_config['flags']
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()
        #close file
        file.close()
        print("Flags updated in JSON file.")

def clearNewMessageGUIFlag(file_path):
    """Clear the NewMessageGUI flag in the JSON file."""
    with open(file_path, 'r+') as file:
        data = json.load(file)
        data['flags']['NewMessageGUI'] = False
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()
        #close file
        file.close()
        print("NewMessageGUI flag cleared in JSON file.")

def clearDrifterIdleFlag(file_path):
    """Clear the DrifterIdle flag in the JSON file to indicate processing is ongoing."""
    file = None
    try:
        with open(file_path, 'r+') as file:
            data = json.load(file)
            data['flags']['DrifterIdle'] = False
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
            file.flush()
            os.fsync(file.fileno())  # Ensures that changes are physically written to disk
            print("DrifterIdle flag cleared")
    except Exception as e:
        print(f"Error clearing DrifterIdle flag: {e}")
    finally:
        if file:
            file.close()

def setDrifterIdleFlag(file_path):
    """Set the DrifterIdle flag in the JSON file to indicate device is idle."""
    try:
        with open(file_path, 'r+') as file:
            data = json.load(file)
            data['flags']['DrifterIdle'] = True
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
            print("DrifterIdle flag set");
    except Exception as e:
        print(f"Error setting DrifterIdle flag: {e}")
    finally:
        if file:
            file.close()

def pullCommands(file_path):
    """Load the commands from the JSON file and update the global dictionary."""
    with open(file_path, 'r') as file:
        data = json.load(file)
        global_config['commands'] = data['commands']
        #close file
        file.close()
        print("Commands pulled from JSON file and updated in global dictionary.")
        
#Reset commands to default values in JSON file except for pumpAction
def resetCommands(file_path):
    """Reset the commands to default values in the JSON file."""
    with open(file_path, 'r+') as file:
        data = json.load(file)
        data['commands']['tareVolume'] = False
        data['commands']['applySettings'] = False
        data['commands']['fetchSettings'] = False
        data['commands']['downloadData'] = False
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()
        #close file
        file.close()
        print("Commands reset to default values in JSON file.")

def getSensorValues(ser):
    #Execute pollSensors function from SeiralInterface.py
    sensor_data =  dserial.pollSensors(ser)

    #Save sensor value to global config dictionary
    global_config['status']['batteryVoltage'] = sensor_data['batteryVoltage']
    global_config['status']['depth'] = sensor_data['depth']
    global_config['status']['temperature'] = sensor_data['temperature']
    global_config['status']['pitch'] = sensor_data['pitch']
    global_config['status']['roll'] = sensor_data['roll']
    global_config['status']['pumpSpeed'] = sensor_data['pumpSpeed']
    global_config['status']['volumeDisplaced'] = sensor_data['volumeDisplaced']
    global_config['status']['internalVolume'] = sensor_data['internalVolume']


#Print status in global config dictionary
def printStatus():
    """Print the current status from the global dictionary."""
    print("Current status:")
    for key, value in global_config['status'].items():
        print(f"{key}: {value}")

def printFlags():
    """Print the current flags from the global dictionary."""
    print("Current flags:")
    for key, value in global_config['flags'].items():
        print(f"{key}: {value}")

def printCommands():
    """Print the current commands from the global dictionary."""
    print("Current commands:")
    for key, value in global_config['commands'].items():
        print(f"{key}: {value}")

def shutdown():
    print("Shutting down...")

    #Send system command to shutdown now
    #os.system("shutdown now")

    exit()
    #exit the function

def printserial(ser, text):
    """
    Sends text to the serial port represented by the serial.Serial object.

    Args:
    ser (serial.Serial): The configured serial port object.
    text (str): Text to send.
    """
    # Ensure the text ends with a newline for proper formatting on the receiving end
    if not text.endswith('\r\n'):
        text += '\r\n'

    try:
        # Send the text encoded as UTF-8
        ser.write(text.encode('utf-8'))

    except serial.SerialException as e:
        # Handle errors in case the serial operation fails
        print(f"Failed to write to serial port: {str(e)}")


def main():
    #define variables
    global pumpPower 
    
    pumpPower = True

    #Open Control Serial Port
    ser = configureControlSerialPort()  #Open Control serial port

    #Open Debug serial port
    debug = configureDebugSerialPort()  #Open Debug serial port

    #Make current path same as script path
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    print("Starting...")
    printserial(debug, "Starting...")

    # Load Configurator.json into memory
    configuratorFilePath = "Configurator.json"

    #Display current configurator flags
    pullFlags(configuratorFilePath)
    print("Initial Flags:")
    printFlags()

    # Load registor configuration json file into memory
    configFilePath = "drifter.cfg"
    configData = load_json(configFilePath)

    #flush serial buffer
    ser.flushInput()

    #Enter command prompt mode
    print("Enter Command Prompt Mode")
    printserial(debug, "Enter Command Prompt Mode")
    dserial.enterTerminalMode(ser)

    print("Start main interface loop")
    printserial(debug, "Start main interface loop")

    #Main loop: Loop until Shutdown flag is set
    while not global_config['flags']['Shutdown']:
        
        #1. Check for new flags and update commands
        pullFlags(configuratorFilePath)

        #Print Flags
        printFlags()

        #2. Check for new commands if newMessageGUI is set
        if global_config['flags']['NewMessageGUI']:
            pullCommands(configuratorFilePath)
            global_config['flags']['NewMessageGUI'] = False
            
            print("New Commands Received")
            #Print Commands
            printCommands()

            #2b. Clear Drifter Idle Flag 
            clearDrifterIdleFlag(configuratorFilePath)

            #2b. Set pump to commanded action
            if global_config['commands']['pumpAction'] == 'in':
                #if pump is off turn on
                if not pumpPower:
                    dserial.togglePumpPower(ser)
                    pumpPower = True
                dserial.pumpIn(ser)
            elif global_config['commands']['pumpAction'] == 'out':
                #if pump is off turn on
                if not pumpPower:
                    dserial.togglePumpPower(ser)
                    pumpPower = True
                dserial.pumpOut(ser)
            elif global_config['commands']['pumpAction'] == 'stop':
                dserial.pumpStop(ser)
                #if Pump is on turn it off
                if pumpPower:
                    dserial.togglePumpPower(ser)
                    pumpPower = False

            #2c. Tare Volume if command is set
            if global_config['commands']['tareVolume']:
                dserial.tareScale(ser)

            #2d. Apply settings if command is set
            if global_config['commands']['applySettings']:
                configData = load_json(configFilePath)
                applySettings(ser, configData)

            #2e. Fetch settings if command is set
            if global_config['commands']['fetchSettings']:
                fetchSettings(ser, configData)
                print("Settings Fetched: Writing to JSON file")
                write_json(configData, configFilePath)

            #2f. Download depth log
            if global_config['commands']['downloadData']:
                datalog_dir = "/home/ssr/Share/Data/"
                current_time_ctime = time.ctime()
                time_struct = time.strptime(current_time_ctime, "%a %b %d %H:%M:%S %Y")
                filename = time.strftime("Depthlog_%Y%m%d-%H%M%S.csv", time_struct)
                full_path = os.path.join(datalog_dir, filename)
                print(f"Downloading Depth Log to {filename}")
                downloadDepthLog.download_drifter(ser, full_path)

            #New Commands Updated Clear NewMessageGUI flag
            clearNewMessageGUIFlag(configuratorFilePath)

            #Reset commands to default values
            resetCommands(configuratorFilePath)

            #Set Drifter Idle Flag
            setDrifterIdleFlag(configuratorFilePath)
        else:
            #No commands received poll and display sensor data
            getSensorValues(ser)
            printStatus()

            #Update Global Config File
            pushStatus(configuratorFilePath)
        
        #Wait 3 seconds
        time.sleep(3)
    
    #If Pump Power On Toggle Pump Power
    if pumpPower:
        dserial.togglePumpPower(ser)
        pumpPower = False

    #Shutdown
    shutdown()


if __name__ == '__main__':
    main()