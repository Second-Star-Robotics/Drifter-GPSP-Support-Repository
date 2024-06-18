#python functions to communicate with Drifter Controller

import serial
import time
import re

#Getline function
def getLine(ser):
    line = ser.readline()
    line_str = line.decode('utf-8')
    stripped_str = line_str.rstrip('\r\n') 
    return stripped_str

import serial
import time

def readTilPrompt(ser, prompt=">> ", post_prompt_timeout=0.1):
    buffer = ''
    while True:
        char = ser.read(1)  # Read one byte at a time
        if char:  # If the byte is not empty
            char_decoded = char.decode('utf-8')  # Decode to string
            buffer += char_decoded  # Add the char to the buffer
            if buffer.endswith(prompt):  # Check if the end of the buffer matches the prompt
                #print("Potential prompt found. Buffer:", buffer)
                time.sleep(post_prompt_timeout)  # Wait to see if more data is coming
                if ser.in_waiting == 0:  # Check if there's no more data coming
                    #print("Confirmed end of data with prompt. Buffer:", buffer)
                    return buffer
        else:
            #print("No more data. Prompt not found. Buffer:", buffer)
            break

    return buffer  # Return what has been read so far (might not end with prompt)

#Parse serial data return from a read command 
#eg.
#>> r1
#3 <--------Value
#>> 
#Read serial data until buffer is empty and parse the value

def readValueTillCommandPrompt(ser):
    value = ''
    while True:
        line = getLine(ser)
        if line == ">> ":
            break
        else:
            value = line
    return value

#Enter terminal command prompt mode
#Send a CR if "Press 'p' for command prompt..." is received send a 'p' character
#if not readTilCommandPrompt
def enterTerminalMode(ser):
    #Clear serial Buffer
    print("Clearing serial buffer")
    ser.flushInput()

    #Send a CR
    print("Sending a CR")
    ser.write(b'\r')
    
    #Wait 100 ms
    print("Waiting 100ms")
    time.sleep(0.1)

    #check for "Press 'p' for command prompt..." if received send a 'p' character
    print("Checking for 'Press 'p' for command prompt...'")
    terminalModeFlag = False

    while terminalModeFlag == False:
        line = getLine(ser)

        #Check if line contains 'Press 'p' for command prompt...'
        if "Press 'p' for command prompt..." in line:
            print("Prompt Received. Sending 'p' character")
            #Send a 'p' character followed by a CR
            ser.write(b'p')
            ser.write(b'\r')
            ser.write(b'p')
            ser.write(b'\r')
            terminalModeFlag = True
        else:
            print("No prompt received. Reading till prompt")
            readTilPrompt(ser)
            terminalModeFlag = False

        time.sleep(5)
 
    print("Reading till prompt")
    readTilPrompt(ser)
    
    print("Entered terminal mode")

#Write an integer register to Drifter 'w<register number> <integer value>'
def writeRegisterInt(ser, register, value):
    # Convert integers to bytes
    register_bytes = str(register).encode('utf-8')
    value_bytes = str(value).encode('utf-8')

    # Send a serial command to write register
    #print ("Writing register: ", register, " with value: ", value)
    ser.write(b'w')
    ser.write(register_bytes)
    ser.write(b' ')
    ser.write(value_bytes)
    ser.write(b'\r')

    #print("Reading till prompt")
    readTilPrompt(ser)


#Read an integer register from Drifter 'r<register number>'
#pass an integer register to read
#return integer value
def readRegisterInt(ser, register):
    # Convert the integer register to bytes
    register_bytes = str(register).encode()

    # Send a serial command to read register
    ser.write(b'r')
    ser.write(register_bytes)
    ser.write(b'\r')

    # Read the response value till command prompt
    value = int(readValueTillCommandPrompt(ser))
    return value

#Write an float register to Drifter 'w<register number> <float value>'
def writeRegisterFloat(ser, register, value):
    # Convert register and value to bytes
    register_bytes = str(register).encode('utf-8')
    value_bytes = str(value).encode('utf-8')

    # Send a serial command to write register
    ser.write(b'w')       # Command to write
    ser.write(register_bytes)
    ser.write(b' ')       # Space separator
    ser.write(value_bytes)
    ser.write(b'\r')      # Carriage return to execute the command

    # Wait for prompt to confirm the operation completed
    readTilPrompt(ser)


#Read a float register from Drifter 'r<register number>'
#pass an integer register to read
#return float value
def readRegisterFloat(ser, register):
    # Convert the integer register to bytes
    register_bytes = str(register).encode()

    # Send a serial command to read register
    ser.write(b'r')
    ser.write(register_bytes)
    ser.write(b'\r')

    # Read the response value till command prompt
    value = float(readValueTillCommandPrompt(ser))
    return value

#Read string from register 404
def readHeader(ser):
    # Send a serial command to read register
    ser.write(b'r404')
    ser.write(b'\r')

    # Read the response value till command prompt
    value = readValueTillCommandPrompt(ser)
    return value

#Write float value to register 404
def writeHeader(ser, value):
    # Encode the string value to bytes
    value_bytes = value.encode('utf-8')

    # Send a serial command to write register
    ser.write(b'w404 ')
    ser.write(value_bytes)
    ser.write(b'\r')
    readTilPrompt(ser)

#Configure serial port using hard coded values and pass serial object
def configureSerialPort():
    #Configurate Commport to COM8
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

#Pump Commands.  Send w255 -200000 to pump in
def pumpIn(ser):
    #Send a serial command to write register
    ser.write(b'w255 -200000\r')
    readTilPrompt(ser)
    print("Pumping in")

def pumpOut(ser):
    #Send a serial command to write register
    ser.write(b'w255 200000\r')
    readTilPrompt(ser)
    print("Pumping out")

def pumpStop(ser):
    #Send a serial command to write register
    ser.write(b'w255 0\r')
    readTilPrompt(ser)
    print("Pump stopped")

#Toggle Pump power with the 'p' serial command
def togglePumpPower(ser):
    #Send a serial command to write register
    ser.write(b'p\r')
    time.sleep(5)
    readTilPrompt(ser)
    print("Pump power toggled")

#Tare Drifter scale with the 'c' command
def tareScale(ser):
    #Send a serial command to write register
    ser.write(b'c\r')
    time.sleep(2)
    readTilPrompt(ser)
    print("Scale tared")

def downloadSamples(serial_port, total_samples):
    global_config['flags']['DrifterIdle'] = False
    last_push_time = time.time()
    
    for i in range(1, total_samples + 1):
        sample = get_sample(serial_port, i)
        print(f"Downloaded sample {i}: {sample}")  # Or process the sample as needed
        global_config['status']['samplesdownloaded'] += 1

        current_time = time.time()
        # Check if 10 seconds have passed since the last status push
        if current_time - last_push_time >= 10:
            pushStatus()
            last_push_time = current_time

    global_config['flags']['DrifterIdle'] = True
    pushStatus()  # Final push to update the status at the end of the download


#get_sample downloads a sample from the serial port
def get_sample(serial_port, sample_number):
    """
    Download a data sample from a serial port.
    
    Args:
    serial_port (serial.Serial): The serial port connected to the device.
    sample_number (int): The sample number to collect.
    
    Returns:
    dict: A dictionary containing the parsed sample data.
    """
    # Define the offset for the sample number (adjust as necessary)
    sample_offset = 405
    
    # Send sample request
    command_str = f'r{sample_offset + sample_number}'
    serial_port.write(command_str.encode() + b'\r\n')
    
    # Wait for the device to start sending data
    time.sleep(1)  # Adjust this based on the expected response time
    
    # Read the response data
    responses = []
    for _ in range(47):  # Number of data points expected
        line = serial_port.readline().decode().strip()
        responses.append(float(line))

    # Parse the responses into a structured dictionary
    return {
        'Timestamp': responses[0],
        'Depth': responses[22],
        'Temperature': responses[23],
        'Battery': responses[24],
        'VOS': responses[25],
        'RangeTime': responses[26],
        'RangeDist': responses[27],
        'USBLAzimuth': responses[28],
        'USBLElevation': responses[29],
        'USBLFitError': responses[30],
        'PositionEasting': responses[31],
        'PositionNorthing': responses[32],
        'PositionDepth': responses[33],
        'AUX': responses[34:44],
        'SrcID': responses[44],
        'ControlState': responses[45],
        'ValveIndex': responses[46],
        'EnablePump': responses[47]
    }

def pollSensors(ser):
    """Poll the sensors and update the global dictionary with the latest sensor data."""

    # Command to request sensor data
    ser.write(b'd')
    ser.write(b'\r')

    time.sleep(5)

    # Read response from serial port
    response = ser.read_until(b'>>').decode()
    
    # Define a dictionary to hold sensor values
    sensor_data = {
        "batteryVoltage": 0.0,
        "depth": 0.0,
        "temperature": 0.0,
        "pitch": 0.0,
        "roll": 0.0,
        "pumpSpeed": 0.0,
        "volumeDisplaced": 0.0,
        "internalVolume": 0.0,
    }

    # Regular expressions to extract sensor data
    patterns = {
        "batteryVoltage": r"Battery\s*:\s*([-0-9.]+)\s*V",
        "depth": r"Depth\s*:\s*([-0-9.]+)\s*m",
        "temperature": r"Temperature\s*:\s*([-0-9.]+)\s*C",
        "pitch": r"Pitch\s*:\s*([-0-9.]+)\s*deg",
        "roll": r"Roll\s*:\s*([-0-9.]+)\s*deg",
        "pumpSpeed": r"Pump Speed\s*:\s*([-0-9.]+)\s*mL/s",
        "volumeDisplaced": r"Volume Displaced\s*:\s*([-0-9.]+)\s*mL",
        "internalVolume": r"Internal Volume\s*:\s*([-0-9.]+)\s*mL",
    }

    # Extract data using regex
    for key, pattern in patterns.items():
        match = re.search(pattern, response)
        if match:
            sensor_data[key] = float(match.group(1))
        
    return sensor_data

def main():
    #Loop to display serial line data <string>+CRLF
    #Configurate Commport to COM8
    ser = configureSerialPort()
    
    #clear serial buffer
    ser.flushInput()

    #Enter command prompt mode
    enterTerminalMode(ser)
    
    #Read register 166
    print("Reading register 166")
    value = readRegisterInt(ser, 166)
    print("Register 166 value: ", value)


if __name__ == '__main__':
    main()
