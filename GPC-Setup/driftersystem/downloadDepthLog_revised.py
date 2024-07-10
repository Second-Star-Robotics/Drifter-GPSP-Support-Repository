import serial
import csv
import time
from datetime import datetime
from SerialInterface import enterTerminalMode, readValueTillCommandPrompt, readRegisterInt, readTilPrompt

def get_sample(serial_conn, sample_number):
    sample_off = 406  # Offset for the first sample
    command_str = f"r{sample_off + sample_number}"
    serial_conn.write(f"{command_str}\r".encode())

    # Read Until prompt
    buffer = readTilPrompt(serial_conn)
    
    # Extract data from buffer ignoring the first line and the last line
    serial_data = buffer.split("\n")[1:-1]
    
    #Extract data from the serial data into the following categories
    # 1. Ticks
    # 2. z_setpoint
    # 3. z_actual (estimated)
    # 4. z_p
    # 5. z_i
    # 6. z_d
    # 7. w_command
    # 8. w_actual (estimated)
    # 9. w_i
    # 10. Nabla_command
    # 11. Nabla_actual
    # 12. Nabla_p
    # 13. Nabla_i
    # 14. Nabla_d
    # 15. Qv_command
    # 16. sps_command
    # 17. Nabla_air
    # 18. Roll
    # 19. Pitch
    # 20. Yaw
    # 21. Scale Derived Oil Volume
    # 22. Depth (raw)
    # 23. Temperature
    # 24. Battery
    # 25. VOS
    # 26. RangeTime
    # 27. RangeDist
    # 28. USBLAzimuth
    # 29. USBLElevation
    # 30. USBLFitError
    # 31. PositionEasting
    # 32. PositionNorthing
    # 33. PositionDepth
    # 34. AUX0
    # 35. AUX1
    # 36. AUX2
    # 37. AUX3
    # 38. AUX4
    # 39. AUX5
    # 40. AUX6
    # 41. AUX7
    # 42. AUX8
    # 43. AUX9
    # 44. SrcID
    # 45. State
    # 46. VALVE_INDEX
    # 47. EN_PUMP
    
    sample = {
        "Ticks": int(serial_data[0]),
        "z_setpoint": float(serial_data[1]),
        "z_actual": float(serial_data[2]),
        "z_p": float(serial_data[3]),
        "z_i": float(serial_data[4]),
        "z_d": float(serial_data[5]),
        "w_command": float(serial_data[6]),
        "w_actual": float(serial_data[7]),
        "w_i": float(serial_data[8]),
        "Nabla_command": float(serial_data[9]),
        "Nabla_actual": float(serial_data[10]),
        "Nabla_p": float(serial_data[11]),
        "Nabla_i": float(serial_data[12]),
        "Nabla_d": float(serial_data[13]),
        "Qv_command": float(serial_data[14]),
        "sps_command": float(serial_data[15]),
        "Nabla_air": float(serial_data[16]),
        "Roll": float(serial_data[17]),
        "Pitch": float(serial_data[18]),
        "Yaw": float(serial_data[19]),
        "Scale Derived Oil Volume": float(serial_data[20]),
        "Depth (raw)": float(serial_data[21]),
        "Temperature": float(serial_data[22]),
        "Battery": float(serial_data[23]),
        "VOS": float(serial_data[24]),
        "RangeTime": float(serial_data[25]),
        "RangeDist": float(serial_data[26]),
        "USBLAzimuth": float(serial_data[27]),
        "USBLElevation": float(serial_data[28]),
        "USBLFitError": float(serial_data[29]),
        "PositionEasting": float(serial_data[30]),
        "PositionNorthing": float(serial_data[31]),
        "PositionDepth": float(serial_data[32]),
        "AUX0": float(serial_data[33]),
        "AUX1": float(serial_data[34]),
        "AUX2": float(serial_data[35]),
        "AUX3": float(serial_data[36]),
        "AUX4": float(serial_data[37]),
        "AUX5": float(serial_data[38]),
        "AUX6": float(serial_data[39]),
        "AUX7": float(serial_data[40]),
        "AUX8": float(serial_data[41]),
        "AUX9": float(serial_data[42]),
        "SrcID": float(serial_data[43]),
        "State": float(serial_data[44]),
        "VALVE_INDEX": float(serial_data[45]),
        "EN_PUMP": float(serial_data[46])
    }
    
    return sample

#Pass the serial object, filename, and the gpiob object for the shutdown flag (GPIO)
def download_drifter(serial_conn, filename):
    # Get total samples from register 166 using readRegisterInt
    n_samples = readRegisterInt(serial_conn, 166)

    print(f"Downloading {n_samples} samples")

    # Open a CSV file to write the data
    with open (filename, 'w', newline='') as csvfile:
        fieldnames = ["Ticks", "z_setpoint", "z_actual", "z_p", "z_i", "z_d", "w_command", "w_actual", "w_i", "Nabla_command", "Nabla_actual", "Nabla_p", "Nabla_i", "Nabla_d", "Qv_command", "sps_command", "Nabla_air", "Roll", "Pitch", "Yaw", "Scale Derived Oil Volume", "Depth (raw)", "Temperature", "Battery", "VOS", "RangeTime", "RangeDist", "USBLAzimuth", "USBLElevation", "USBLFitError", "PositionEasting", "PositionNorthing", "PositionDepth", "AUX0", "AUX1", "AUX2", "AUX3", "AUX4", "AUX5", "AUX6", "AUX7", "AUX8", "AUX9", "SrcID", "State", "VALVE_INDEX", "EN_PUMP"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
    
    for sample_index in range(n_samples):
        sample = get_sample(serial_conn, sample_index)

        #Give Status update by printing the sample every 100 samples (eg. sample n of m samples)
        if sample_index % 100 == 0:
            print(f"Sample {sample_index} of {n_samples}")

        # Append sample to CSV file
        with open (filename, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(sample)

        #Close the file
        csvfile.close()

def download_drifter_subset(serial_conn, filename, start_sample, end_sample):
    print(f"Downloading samples from {start_sample} to {end_sample}")

    # Open a CSV file to write the data
    with open (filename, 'w', newline='') as csvfile:
        fieldnames = ["Ticks", "z_setpoint", "z_actual", "z_p", "z_i", "z_d", "w_command", "w_actual", "w_i", "Nabla_command", "Nabla_actual", "Nabla_p", "Nabla_i", "Nabla_d", "Qv_command", "sps_command", "Nabla_air", "Roll", "Pitch", "Yaw", "Scale Derived Oil Volume", "Depth (raw)", "Temperature", "Battery", "VOS", "RangeTime", "RangeDist", "USBLAzimuth", "USBLElevation", "USBLFitError", "PositionEasting", "PositionNorthing", "PositionDepth", "AUX0", "AUX1", "AUX2", "AUX3", "AUX4", "AUX5", "AUX6", "AUX7", "AUX8", "AUX9", "SrcID", "State", "VALVE_INDEX", "EN_PUMP"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

    for sample_index in range(start_sample, end_sample + 1):
        sample = get_sample(serial_conn, sample_index)

        # Give status update by printing the sample every 100 samples (e.g., sample n of m samples)
        if sample_index % 100 == 0:
            print(f"Sample {sample_index} of {end_sample}")

        # Append sample to CSV file
        with open (filename, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(sample)

        # Close the file
        csvfile.close()
        
        #Delay 0.1 seconds
        time.sleep(0.1)

def main():
    ser = serial.Serial('/dev/ttyS2', 57600, timeout=0.3)  # Changed timeout from 0.1 to 0.3 to allow for longer response times
    first_timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"/home/ssr/Share/Data/Depth_Log_{first_timestamp}.csv"

    starting_sample = 1
    ending_sample = 1000

    print("Downloading Samples from sample " + str(starting_sample) + " to sample " + str(ending_sample))

    download_drifter_subset(ser, filename, starting_sample, ending_sample)

    print("Download Complete")

if __name__ == '__main__':
    main()
