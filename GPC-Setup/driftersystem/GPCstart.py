# GPIO used PA17

import gpiod
import time
import serial
import os
import datetime
import re
import jsonInterface

#Set datalog directory
datalog_dir = "/home/ssr/Share/Data/"
csv_file = None  # Global variable for the CSV file
file_handle = None

#Configure serial port using hard coded values and pass serial object (tty2)
def configureControlSerialPort():
    #Configurate Commport
    Commport = '/dev/ttyS2'
    baudrate = 57600
    timeout = 10
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

#Configure serial port using hard coded values and pass serial object for GPS (tty1)
def configureSensorSerialPort():
    #Configurate Commport
    Commport = '/dev/ttyS1'
    baudrate = 19200
    timeout = 0.5
    stopbits = 1
    bytesize = 8
    parity = 'N'
    xonxoff = False
    flowcontrol = False

    ser = serial.Serial(Commport, baudrate, timeout=timeout, stopbits=stopbits, bytesize=bytesize, parity=parity, xonxoff=xonxoff, rtscts=flowcontrol, dsrdtr=flowcontrol)

    return ser
import re

#Read and extract the epoch time from the Drifter controller
def extract_epoch_time(ser, debug):
    try:
        # Read the data from the serial port and append to the character array until a '$' and then a '%' is found
        serial_data1 = ser.read_until(b'$').decode('utf-8')
                        
        serial_data2 = ser.read_until(b'%').decode('utf-8')

        serial_data = serial_data1 + serial_data2
        
        # Regular expression to find the pattern $epochtime%
        pattern = r'\$(\d+)%'
        match = re.search(pattern, serial_data)
        
        if match:
            # Extract and return the epoch time as an integer
            epoch_time = int(match.group(1))
            return epoch_time
        else:
            return None
    except serial.SerialException as e:
        print(f"Failed to read from serial port: {str(e)}")
        printserial(debug, f"Failed to read from serial port: {str(e)}")
        return None

#Set the current system time with the provided epoch time    
def setTime(epoch_time, debug):
    """
    Sets the current system time using the provided epoch time (in UTC).

    Args:
    epoch_time (int): The epoch time to set the system time to.
    debug (serial.Serial): Optional serial port object for debugging messages.
    """
    # Convert epoch time to datetime object in UTC
    dt = datetime.datetime.utcfromtimestamp(epoch_time)
    
    # Format the datetime object to a string suitable for the `date` command
    date_str = dt.strftime('%m%d%H%M%Y.%S')
    
    # Set the system time using the `date` command
    os.system(f'sudo date {date_str}')
    
    # Synchronize the hardware clock with the system time
    os.system('sudo hwclock -w')
    
    # Verify and print the system time
    os.system('date')
    os.system('sudo hwclock -r')

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

    #s

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
    
def main():
    #Loop to display serial line data <string>+CRLF
    #Configurate Commport to COM8
    #ser = configureSerialPort()

    global file_handle

    #Initialize the debug serial port
    debug = configureDebugSerialPort()

    #Initialize the sensor serial port
    sensor = configureSensorSerialPort()

    #Initialize the control serial port
    control = configureControlSerialPort()

    #Starting Script
    print("==============================================")
    print("Starting the GPSstart daemon...")
    printserial(debug, "==============================================")
    printserial(debug, "Starting the GPSstart daemon...")
    
    #Open the GPIO chip    
    chip = gpiod.Chip('gpiochip0')

    #Configure the GPIO Line PB11 as output called IDLE_FLAG
    GPIO_Name = "PB11"
    line = chip.find_line(GPIO_Name)  # Get the line by name directly if supported
    IDLE_FLAG = chip.get_lines([line.offset()])
    print("Offset: ", line.offset())
    IDLE_FLAG.request(consumer='foobar', type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0])

    #Configure the GPIO Line to PB12 as an input SHUTDOWN_FLAG
    GPIO_Name = "PB12"
    line = chip.find_line(GPIO_Name)  # Get the line by name directly if supported
    SHUTDOWN_FLAG = chip.get_lines([line.offset()])
    print("Offset: ", line.offset())
    SHUTDOWN_FLAG.request(consumer='foobar', type=gpiod.LINE_REQ_DIR_IN)
    
    #Configure the GPIO Line PD11 as an input MODE_FLAG
    GPIO_Name = "PD11"
    line = chip.find_line(GPIO_Name)  # Get the line by name directly if supported
    MODE_FLAG = chip.get_lines([line.offset()])
    print("Offset: ", line.offset())
    MODE_FLAG.request(consumer='foobar', type=gpiod.LINE_REQ_DIR_IN)

    #Configure the GPIO Line to PD19 as an output
    GPIO_Name = "PD19"
    line = chip.find_line(GPIO_Name)  # Get the line by name directly if supported
    PD19 = chip.get_lines([line.offset()])
    print("Offset: ", line.offset())
    PD19.request(consumer='foobar', type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0])

    #Configure the GPIO Line to PD20 as an output
    GPIO_Name = "PD20"
    line = chip.find_line(GPIO_Name)  # Get the line by name directly if supported
    RECORD_FLAG = chip.get_lines([line.offset()])
    print("Offset: ", line.offset())
    RECORD_FLAG.request(consumer='foobar', type=gpiod.LINE_REQ_DIR_IN)

    #Set Initial Flag Values
    print("Set IDLE_FLAG = 0")
    printserial(debug, "Set IDLE_FLAG = 0")
    IDLE_FLAG.set_values([0])

    #Get Datetime from controller
    print("Get Date and Time from Controller...")
    printserial(debug, "Get Date and Time from Controller...")

    #Collect serial data and append to character array until a '$' and then a '%' is found
    #Try to extract the epoch time from the serial data 10 times
    for i in range(10):
        epoch_time = extract_epoch_time(control, debug)
        if epoch_time is not None:
            break
        time.sleep(1)

    print("Epoch Time: " + str(epoch_time))
    printserial(debug, "Epoch Time: " + str(epoch_time))
    
    setTime(epoch_time, debug)
    
    previous_record_flag = False

    #Main Loop
    print("Starting the loop...")
    printserial(debug, "Starting the loop...")
    while True: 
        #Set Idle Flag to 0
        IDLE_FLAG.set_values([0])

        #print("----------------------------------------------")
        printserial(debug, "----------------------------------------------")

        #Display current date and time
        #print("Logger Date and Time: " + time.ctime())
        printserial(debug, "Logger Date and Time: " + time.ctime())

        #Display Status of output Flags
        idleFlag = IDLE_FLAG.get_values()[0]
        if (idleFlag):
            #print("IDLE_FLAG: True")
            printserial(debug, "IDLE_FLAG: True")
        else:
            #print("IDLE_FLAG: False")
            printserial(debug, "IDLE_FLAG: False")
        
        #Read flags from the controller and display them
        #print("Read Controller Flags...")
        printserial(debug, "Read Controller Flags...")
        #Read Mode Flag
        modeFlag = MODE_FLAG.get_values()[0]
        if (modeFlag):
            #print("MODE_FLAG: True")
            printserial(debug, "MODE_FLAG: True")

            #Start jsonInterface.py (in current diredtory)
            print("Starting jsonInterface.py...")
            printserial(debug, "Starting jsonInterface.py...")

            #Close serial ports to allow jsonInterface to use them
            control.close()
            sensor.close()
            debug.close()
            os.system("sudo python3 /home/ssr/Share/driftersystem/jsonInterface.py")
        else:
            #print("MODE_FLAG: False")
            printserial(debug, "MODE_FLAG: False")

        #Read Shutdown Flag
        shutdownFlag = SHUTDOWN_FLAG.get_values()[0]
        if (shutdownFlag):
            #print("SHUTDOWN_FLAG: True")
            printserial(debug, "SHUTDOWN_FLAG: True")
        else:
            #print("SHUTDOWN_FLAG: False")
            printserial(debug, "SHUTDOWN_FLAG: False")

        if (shutdownFlag):
            print("Shutdown Flag detected...")
            printserial(debug, "Shutdown Flag detected...")

            #Flush internal buffer to OS
            if file_handle:
                file_handle.flush()
                os.fsync(file_handle.fileno())
                print("Flushed file")
                printserial(debug, "Flushed file")

                os.sync()
                print("Synced file")
                printserial(debug, "Synced file")

                file_handle.close()
                print("Closed file")
                printserial(debug, "Closed file")

                #Delay 5 seconds
                time.sleep(5)            

            print("Shutting Down...")
            printserial(debug, "Shutting Down...")
            #Send Shutdown now command via os command
            os.system("sudo shutdown now")
            break

            # Initialize the previous record flag state as False (assuming low initially)

        #Read Record Flag
        recordFlag = RECORD_FLAG.get_values()[0]
        if recordFlag:
            #print("RECORD_FLAG: True")
            printserial(debug, "RECORD_FLAG: True")
            # Check if the record flag has just been switched from low to high
            if not previous_record_flag:
                # Open a new CSV file with the current date and time as the filename with datalog directory
                current_time_ctime = time.ctime()
                time_struct = time.strptime(current_time_ctime, "%a %b %d %H:%M:%S %Y")
                filename = time.strftime("%Y%m%d-%H%M%S.txt", time_struct)
                full_path = os.path.join(datalog_dir, filename)
                file_handle = open(full_path, 'w')  # Open file in write mode
                
                #print Open File and print filename with full path
                print("Opened file: " + full_path)
                printserial(debug, "Opened file: " + full_path)
                                
            #Append serial data on the sensor port to the file
            if file_handle:
                # Display all serial data from the sensor currently in the buffer
                sensor_data = sensor.read(sensor.in_waiting).decode('utf-8')
                                
                #print(sensor_data)
                printserial(debug, sensor_data)

                #Append current data to the end of the file
                file_handle.write(sensor_data)
            
        else:
            #print("RECORD_FLAG: False")
            printserial(debug, "RECORD_FLAG: False")
            #Check if the record flag has just been switched from high to low
            if previous_record_flag:
                # Update the previous record flag to current state
                if file_handle:
                    file_handle.flush()
                    os.fsync(file_handle.fileno())
                    print("Flushed file")
                    printserial(debug, "Flushed file")

                    os.sync()
                    print("Synced file")
                    printserial(debug, "Synced file")

                    file_handle.close()
                    print("Closed file")
                    printserial(debug, "Closed file")

                    #Delay 5 seconds
                    time.sleep(5)   
        
                    
        # Update the previous record flag to current state
        previous_record_flag = recordFlag
            

        time.sleep(1)
        

if __name__ == '__main__':
    main()