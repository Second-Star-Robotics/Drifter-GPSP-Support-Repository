import serial
import csv
import time
from datetime import datetime
from SerialInterface import enterTerminalMode, readValueTillCommandPrompt, readRegisterInt, readTilPrompt

startsample = 0

def get_sample(serial_obj, sample_number):
    """
    Download a data sample.
    
    Parameters:
    serial_obj (serial.Serial): Serial Port Object
    sample_number (int): Number of the sample to collect
    
    Returns:
    dict: Data Structure containing Driftcam control data.
    """
    
    sample_off = 406
    
    # Send sample request string
    command_str = f'r{sample_off + sample_number}\r'
    serial_obj.write(command_str.encode())
    
    n_measurements = 47
    serial_data = []
    measurement_index = 0
    
    # Read the first line to clear it (contains the command echo)
    serial_obj.readline()
    
    # Read the required number of measurements
    while measurement_index < n_measurements:
        measurement_index += 1
        serial_data.append(serial_obj.readline().decode().strip())
    
    # Parse the serial data into the Sample dictionary
    Sample = {
        'Ticks': float(serial_data[0]),  # 1. Ticks
        'z_setpoint': float(serial_data[1]),  # 2. z_setpoint
        'z_actual': float(serial_data[2]),  # 3. z_actual (estimated)
        'z_p': float(serial_data[3]),  # 4. z_p
        'z_i': float(serial_data[4]),  # 5. z_i
        'z_d': float(serial_data[5]),  # 6. z_d
        'w_command': float(serial_data[6]),  # 7. w_command
        'w_actual': float(serial_data[7]),  # 8. w_actual (estimated)
        'w_i': float(serial_data[8]),  # 9. w_i
        'Nabla_command': float(serial_data[9]),  # 10. Nabla_command
        'Nabla_actual': float(serial_data[10]),  # 11. Nabla_actual
        'Nabla_p': float(serial_data[11]),  # 12. Nabla_p
        'Nabla_i': float(serial_data[12]),  # 13. Nabla_i
        'Nabla_d': float(serial_data[13]),  # 14. Nabla_d
        'Qv_command': float(serial_data[14]),  # 15. Qv_command
        'sps_command': float(serial_data[15]),  # 16. sps_command
        'Nabla_air': float(serial_data[16]),  # 17. Nabla_air
        'Pitch': float(serial_data[17]),  # 18. Pitch
        'Roll': float(serial_data[18]),  # 19. Roll
        'Yaw': float(serial_data[19]),  # 20. Yaw
        'Scale Derived Oil Volume': float(serial_data[20]),  # 21. Scale Derived Oil Volume
        'Depth (raw)': float(serial_data[21]),  # 22. Depth (raw)
        'Temperature': float(serial_data[22]),  # 23. Temperature
        'Battery': float(serial_data[23]),  # 24. Battery
        'VOS': float(serial_data[24]),  # 25. VOS
        'RangeTime': float(serial_data[25]),  # 26. RangeTime
        'RangeDist': float(serial_data[26]),  # 27. RangeDist
        'USBLAzimuth': float(serial_data[27]),  # 28. USBLAzimuth
        'USBLElevation': float(serial_data[28]),  # 29. USBLElevation
        'USBLFitError': float(serial_data[29]),  # 30. USBLFitError
        'PositionEasting': float(serial_data[30]),  # 31. PositionEasting
        'PositionNorthing': float(serial_data[31]),  # 32. PositionNorthing
        'PositionDepth': float(serial_data[32]),  # 33. PositionDepth
        'AUX0': float(serial_data[33]),  # 34. AUX0
        'AUX1': float(serial_data[34]),  # 35. AUX1
        'AUX2': float(serial_data[35]),  # 36. AUX2
        'AUX3': float(serial_data[36]),  # 37. AUX3
        'AUX4': float(serial_data[37]),  # 38. AUX4
        'AUX5': float(serial_data[38]),  # 39. AUX5
        'AUX6': float(serial_data[39]),  # 40. AUX6
        'AUX7': float(serial_data[40]),  # 41. AUX7
        'AUX8': float(serial_data[41]),  # 42. AUX8
        'AUX9': float(serial_data[42]),  # 43. AUX9
        'SrcID': float(serial_data[43]),  # 44. SrcID
        'State': float(serial_data[44]),  # 45. Control State
        'VALVE_INDEX': float(serial_data[45]),  # 46. VALVE_INDEX
        'EN_PUMP': float(serial_data[46]),  # 47. EN_PUMP
    }
    
    return Sample


#Pass the serial object, filename, and the gpiob object for the shutdown flag (GPIO)
def download_drifter(serial_conn, filename, startsample):
    # Get total samples from register 166 using readRegisterInt
    n_samples = readRegisterInt(serial_conn, 166)

    print(f"Downloading {n_samples} samples")

    # Open a CSV file to write the data
    with open (filename, 'w', newline='') as csvfile:
        fieldnames = ["Ticks", "z_setpoint", "z_actual", "z_p", "z_i", "z_d", "w_command", "w_actual", "w_i", "Nabla_command", "Nabla_actual", "Nabla_p", "Nabla_i", "Nabla_d", "Qv_command", "sps_command", "Nabla_air", "Roll", "Pitch", "Yaw", "Scale Derived Oil Volume", "Depth (raw)", "Temperature", "Battery", "VOS", "RangeTime", "RangeDist", "USBLAzimuth", "USBLElevation", "USBLFitError", "PositionEasting", "PositionNorthing", "PositionDepth", "AUX0", "AUX1", "AUX2", "AUX3", "AUX4", "AUX5", "AUX6", "AUX7", "AUX8", "AUX9", "SrcID", "State", "VALVE_INDEX", "EN_PUMP"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

    for sample_index in range(startsample, n_samples-1):

        #Try to get a sample, if error occurs send a CR clear the serial buffer and try again 5 times
        for i in range(5):
            try:
                sample = get_sample(serial_conn, sample_index)
                break
            except:
                serial_conn.write(b'\r')
                #Clear the serial buffer
                readTilPrompt(serial_conn)
                time.sleep(0.5)
                print("Error getting sample, trying again")
                continue

        #Give Status update by printing the sample every 100 samples (eg. sample n of m samples)
        if sample_index % 100 == 0:
            print(f"Sample {sample_index} of {n_samples}")

        # Append sample to CSV file
        with open (filename, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(sample)

        #Close the file
        csvfile.close()

        #Delay to let controller keep up
        #time.sleep(0.1)

def main():
    global startsample

    ser = serial.Serial('/dev/ttyS2', 57600, timeout=3)  # Replace with the appropriate serial port configuration
    first_timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"/home/ssr/Share/Data/Depth_Log_{first_timestamp}.csv"
    download_drifter(ser, filename, startsample)

if __name__ == '__main__':
    main()
