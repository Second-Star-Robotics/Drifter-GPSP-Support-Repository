function exportControlProgram(Data, filename)
%EXPORTCONTROLPROGRAM Export data structure from drifter into sim control
%function exportControlProgram(Data, filename)
%inputs:
%   Data = Data structure generated by downloadDrifter
%   Filename = output filename (example 'DiveControl.csv')
%
%outputs:
%   none
%
%dependencies:
%   csvwrite_with_headers
%
%Eric Berkenpas
%09/20/2022
%
%See also DOWNLOADDRIFTER

nSamples = length([Data.Timestamp]);

%Initialize Output Data Matrix
DataMatrix = zeros(nSamples, 10);

%Generate columns
Time = [Data.Timestamp] - min([Data.Timestamp]); %[s]
Volume = [Data.Nabla_actual]./1000; %[L]
Depth = [Data.Depth]; %[m]
SetVolume = ones(nSamples, 1); %[1 = True, 0 = False]

%Insert into Data Matrix
DataMatrix(:, 1) = Time;
DataMatrix(:, 4) = Depth;
DataMatrix(:, 9) = Volume;
DataMatrix(:, 10) = SetVolume;

%Define Headers
headers = {'Time[s]','Fx[N]','Fy[N]','Depth[m]','Phi[deg]','Theta[deg]', 'Psi[deg]','Control Enable','Volume[L]','Set Volume'};

%Write CSV with headers
csvwrite_with_headers(filename, DataMatrix, headers);
