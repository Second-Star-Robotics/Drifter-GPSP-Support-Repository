function [Data] = loadDrifterCSV2(data_filename)
%LOADDRIFTERCSV load drifter buoyancy engine data from a CSV file.
%function [Data] = loadDrifterCSV(data_filename)
%inputs:
%   data_filename = string containing filename of data
%outputs:
%   Data = structure containing all BC Data.
%
%Eric Berkenpas
%09/20/2022
%
%See also DOWNLOAD_DATA PLOT_DRIFTCAM_DATA

% Read the CSV file and skip the first row
opts = detectImportOptions(data_filename);
opts.DataLines = [2 Inf]; % Start reading from the second line to ignore the header

data_table = readtable(data_filename, opts);

% Convert table to structure
Data = table2struct(data_table, 'ToScalar', true);

% The field names in the structure will match the column names in the CSV file

% For backward compatibility, we can also create individual fields:
Data.Timestamp = data_table.Ticks;
Data.z_setpoint = data_table.z_setpoint;
Data.z_actual = data_table.z_actual;
Data.z_p = data_table.z_p;
Data.z_i = data_table.z_i;
Data.z_d = data_table.z_d;
Data.w_command = data_table.w_command;
Data.w_actual = data_table.w_actual;
Data.w_i = data_table.w_i;
Data.Nabla_command = data_table.Nabla_command;
Data.Nabla_actual = data_table.Nabla_actual;
Data.Nabla_p = data_table.Nabla_p;
Data.Nabla_i = data_table.Nabla_i;
Data.Nabla_d = data_table.Nabla_d;
Data.Qv_command = data_table.Qv_command;
Data.sps_command = data_table.sps_command;
Data.Nabla_air = data_table.Nabla_air;
Data.Pitch = data_table.Pitch;
Data.Roll = data_table.Roll;
Data.Yaw = data_table.Yaw;
Data.Nabla_Scale = data_table.ScaleDerivedOilVolume;
Data.Depth = data_table.Depth_raw_;
Data.Temperature = data_table.Temperature;
Data.Battery = data_table.Battery;
Data.VOS = data_table.VOS;
Data.RangeTime = data_table.RangeTime;
Data.RangeDist = data_table.RangeDist;
Data.USBLAzimuth = data_table.USBLAzimuth;
Data.USBLElevation = data_table.USBLElevation;
Data.USBLFitError = data_table.USBLFitError;
Data.PositionEasting = data_table.PositionEasting;
Data.PositionNorthing = data_table.PositionNorthing;
Data.PositionDepth = data_table.PositionDepth;
Data.AUX0 = data_table.AUX0;
Data.AUX1 = data_table.AUX1;
Data.AUX2 = data_table.AUX2;
Data.AUX3 = data_table.AUX3;
Data.AUX4 = data_table.AUX4;
Data.AUX5 = data_table.AUX5;
Data.AUX6 = data_table.AUX6;
Data.AUX7 = data_table.AUX7;
Data.AUX8 = data_table.AUX8;
Data.AUX9 = data_table.AUX9;
Data.SrcID = data_table.SrcID;
Data.Control_State = data_table.State;
Data.VALVE_INDEX = data_table.VALVE_INDEX;
Data.EN_PUMP = data_table.EN_PUMP;

%figure;
%plot_Driftcam_data(Data);

end
