function saveDrifter(filename, Data)
%SAVEDRIFTER save data downloaded from Driftcam to tab deliminted text file 
%function saveDrifter(filename, Data)
%inputs:
%   filename = Name of text file to save
%   Data = Data structure generated by download_data.m
%
%outputs:
%   none
%
%dependencies:
%
%Eric Berkenpas
%10/06/2023
%
%See also DOWNLOAD_DATA PLOT_DRIFTCAM_DATA

%Extract vectors from Data structure

Timestamp = [Data.Timestamp]'; %1. Timestamp
z_setpoint = [Data.z_setpoint]'; %2. z_setpoint
z_actual = [Data.z_actual]'; %3. z_actual (estimated)
z_p = [Data.z_p]'; %4. z_p
z_i = [Data.z_i]'; %5. z_i
z_d = [Data.z_d]'; %6. z_d
w_command = [Data.w_command]'; %7. w_command
w_actual = [Data.w_actual]'; %8. w_actual (estimated)
w_i = [Data.w_i]'; %9. w_i
Nabla_command = [Data.Nabla_command]'; %10. Nabla_command
Nabla_actual = [Data.Nabla_actual]'; %11. Nabla_actual
Nabla_p = [Data.Nabla_p]'; %12. Nabla_p
Nabla_i = [Data.Nabla_i]'; %13. Nabla_i
Nabla_d = [Data.Nabla_d]'; %14. Nabla_d
Qv_command = [Data.Qv_command]'; %15. Qv_command
sps_command = [Data.sps_command]'; %16. sps_command
Nabla_air = [Data.Nabla_air]'; %17. Nabla_air
Pitch = [Data.Pitch]'; %18. Pitch
Roll = [Data.Roll]'; %19. Roll
Yaw = [Data.Yaw]'; %20. Yaw
Nabla_Scale = [Data.Nabla_Scale]'; %21. Nabla Scale
Depth_raw = [Data.Depth]'; %12. Depth (raw)
Temperature = [Data.Temperature]'; %23. Temperature
Battery = [Data.Battery]'; %24. Battery
VOS = [Data.VOS]'; %25. Velocity of Sound
RangeTime = [Data.RangeTime]'; %26 RangeTime
RangeDist = [Data.RangeDist]'; %27 RangeDist
USBLAzimuth = [Data.USBLAzimuth]'; %28 USBLAzimuth
USBLElevation = [Data.USBLElevation]'; %29. USBLElevation
USBLFitError = [Data.USBLFitError]'; %30. USBLFitError
PositionEasting = [Data.PositionEasting]'; %31. PositionEasting
PositionNorthing = [Data.PositionNorthing]'; %32. PositionNorthing
PositionDepth = [Data.PositionDepth]'; %33. PositionDepth
AUX0 = [Data.AUX0]'; %34. AUX0
AUX1 = [Data.AUX1]'; %35. AUX1
AUX2 = [Data.AUX2]'; %36. AUX2
AUX3 = [Data.AUX3]'; %37. AUX3
AUX4 = [Data.AUX4]'; %38. AUX4
AUX5 = [Data.AUX5]'; %39. AUX5
AUX6 = [Data.AUX6]'; %40. AUX6
AUX7 = [Data.AUX7]'; %41. AUX7
AUX8 = [Data.AUX8]'; %42. AUX8
AUX9 = [Data.AUX9]'; %43. AUX9
SrcID = [Data.SrcID]'; %44. SrcID
Control_State = [Data.Control_State]'; %45. ControL_State
VALVE_INDEX = [Data.VALVE_INDEX]'; %46. VALVE_INDEX
EN_PUMP = [Data.EN_PUMP]'; %47. EN_VALVE

data_matrix = [Timestamp, z_setpoint, z_actual, z_p, z_i, z_d, w_command, w_actual, ...
                w_i, Nabla_command, Nabla_actual, Nabla_p, Nabla_i, Nabla_d, ...
                Qv_command, sps_command, Nabla_air, Pitch, Roll, Yaw, Nabla_Scale, Depth_raw, ...
                Temperature, Battery, VOS, RangeTime, RangeDist, USBLAzimuth, USBLElevation, ...
                USBLFitError, PositionEasting, PositionNorthing, PositionDepth, ...
                AUX0, AUX1, AUX2, AUX3, AUX4, AUX5, AUX6, AUX7, AUX8, AUX9, SrcID, ...
                Control_State, VALVE_INDEX, EN_PUMP];
            
dlmwrite(filename,data_matrix,'delimiter','\t','precision','%.7f');