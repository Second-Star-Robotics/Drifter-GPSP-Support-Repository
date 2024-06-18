function h = plotDrifter(Data)
%PLOTDRIFTER plot data downloaded from Drifter 
%function h = plotDrifter(Data)
%inputs:
%   Data = Data structure generated by download_data.m
%
%outputs:
%   h = figure handle
%
%dependencies:
%
%Eric Berkenpas
%09/20/2022
%
%See also DOWNLOADDRIFTER

%Extract vectors from Data structure
Timestamp = [Data.Timestamp]; %1. Timestamp
z_setpoint = [Data.z_setpoint]; %2. z_setpoint
z_actual = [Data.z_actual]; %3. z_actual (estimated)
z_p = [Data.z_p]; %4. z_p
z_i = [Data.z_i]; %5. z_i
z_d = [Data.z_d]; %6. z_d
w_command = [Data.w_command]; %7. w_command
w_actual = [Data.w_actual]; %8. w_actual (estimated)
w_i = [Data.w_i]; %9. w_i
Nabla_command = [Data.Nabla_command]; %10. Nabla_command
Nabla_actual = [Data.Nabla_actual]; %11. Nabla_actual
Nabla_p = [Data.Nabla_p]; %12. Nabla_p
Nabla_i = [Data.Nabla_i]; %13. Nabla_i
Nabla_d = [Data.Nabla_d]; %14. Nabla_d
Qv_command = [Data.Qv_command]; %15. Qv_command
sps_command = [Data.sps_command]; %16. sps_command
Nabla_air = [Data.Nabla_air]; %17. Nabla_air
Pitch = [Data.Pitch]; %18. Pitch
Roll = [Data.Roll]; %19. Roll
Yaw = [Data.Yaw]; %20. Yaw
Nabla_Scale = [Data.Nabla_Scale]; %21.  Scale Derived Oil Volume
Depth_raw = [Data.Depth]; %12. Depth (raw)
Temperature = [Data.Temperature]; %23. Temperature
Battery = [Data.Battery]; %24. Battery

Control_State = [Data.Control_State]; %25. SG_TEST
VALVE_INDEX = [Data.VALVE_INDEX]; %26. VALVE_INDEX
EN_PUMP = [Data.EN_PUMP]; %47. EN_PUMP

%Process Data
t=Timestamp-Timestamp(1);  %[s] Generate time vector from Timestamp
T_hrs = t./3600;
% encoder_Position_Zeroed = encoder_Position - encoder_Position(1);
Pulses_per_mL = 461163.887; %Pulses per mL
Steps_per_mL = 253325.889; %Stepper pulses per mL
% Delta_Nabla = encoder_Position_Zeroed/Pulses_per_mL; %Engine induced change in volume
Volts_per_ADC = 0.011255364806867; %Volts

%PLOT Depth and Depth Setpoint vs Time
    %Plot

    %Plot Depth
    subplot(2,1,1); 
    plot(T_hrs,Depth_raw,'-k', T_hrs, z_setpoint, '--r'); 
    ax = axis;
    ax(3) = 0; %cut of at surface (z=0.0m)
    axis(ax);
    title('Depth'); 
    xlabel('Time[s]');
    ylabel('Depth [m]'); 
    set(gca,'Ydir','reverse');
    grid on;
    legend('Actual', 'Setpoint');
    
    h(2) = subplot(2,1,2);
    yyaxis left;
    plot(T_hrs, Nabla_actual, '-k', T_hrs, Nabla_command, '--r');;
    set(h(2),'ycolor', 'k')

    grid on;
    ylabel('\Delta Engine Volume [mL]');
    %Plot flow rate
    h(2) = subplot(2,1,2);
    yyaxis right;

    plot(T_hrs, Qv_command, '.b');
    set(h(2),'ycolor', 'b')
    ylabel('Flow Rate [mL/s]');

    legend('Actual', 'Setpoint', 'Flow');

%Plot Buoyancy Controller
    figure;
    %Plot depth control
    subplot(5,1,1); 
    plot(T_hrs, z_actual, '-k', T_hrs, Depth_raw, '-b', T_hrs ,z_setpoint, '--r'); 
    ax = axis;
    ax(3) = 0; %cut of at surface (z=0.0m)
    axis(ax);
    set(gca,'Ydir','reverse');
    title('Depth (z)');
    xlabel('Time[s]');
    ylabel('z [m]'); 
    grid on;
    legend('estimate', 'raw', 'SP');
     
    %Plot depth translation rate
    subplot(5,1,2); 
    %plot(T_hrs, w_actual, '-k', T_hrs, z_d, '-b', T_hrs, w_command,'--r');  
    plot(T_hrs, w_actual, '-k', T_hrs, w_command,'--r');  
    ax = axis;
    if (ax(3)<-0.25)
        ax(3) = -0.25;
    end
    if (ax(4)>0.25)
        ax(4) = 0.25;
    end
    axis(ax);
    set(gca,'Ydir','reverse');
    title('Depth Rate (w)'); 
    xlabel('Time[s]');
    ylabel('Vertical Velocity [m/s]'); 
    grid on;
    legend('estimate', 'Command');

    %Engine Volume (Nabla_eng)
    subplot(5,1,3); 
    plot(T_hrs,Nabla_actual,'-k', T_hrs, Nabla_command,'--r'); 
    title('Volume [V]'); 
    xlabel('Time[s]');
    ylabel('\nabla [mL]'); 
    legend('Actual', 'Command');
    grid on;

    %Offset Adjustment
    Ki_w = -2;
    subplot(5,1,4); 
    plot(T_hrs,w_i*Ki_w ,'-k', T_hrs, Nabla_air, '-b'); 
    title('Volume Offset'); 
    xlabel('Time[s]');
    ylabel('\nabla [mL]');
    legend('offset', 'air volume');
    grid on;

    %Plot Volumetric Flow Rate (Qv)
    subplot(5,1,5); 
    plot(T_hrs, Qv_command); 
    title('Pump Flow Rate'); 
    xlabel('Time [s]'); 
    ylabel('Flow [mL/s]');
    grid on;

    
%PLOT SENSORS
    figure;
    %Battery
    subplot(2,1,1); 
    plot(T_hrs,Battery); 
    title('Battery Level'); 
    grid on; 
    xlabel('Time [s]'); 
    ylabel('Battery [Volts]');
    %Temperature
    subplot(2,1,2);
    plot(T_hrs, Temperature);
    title('Temperature');
    grid on;
    xlabel('Time [s]');
    ylabel('Temperature [C]');

%PLOT OPERATING POINT
    figure; 
    %Error
    subplot(2,1,1);
    plot(T_hrs, abs(z_actual-z_setpoint));
    title('Error');
    grid on;
    xlabel('Time [s]');
    ylabel('z Error [m]');
    %Operating Point
    subplot(2,1,2);
    plot(T_hrs,Control_State);
    grid on;
    xlabel('Time [s]');
    %ylabel('Operating Point');
    yticks([1 2 3 4 5])
    yticklabels({'Control','Hibernate', 'Dive', 'Surface', 'Interval'});

%Oil Volume Derived from Scale
    figure;
    %Plot Depth
    subplot(4,1,1); 
    plot(T_hrs,Depth_raw,'-k', T_hrs, z_setpoint, '--r', T_hrs, z_actual); 
    ax = axis;
    ax(3) = 0; %cut of at surface (z=0.0m)
    axis(ax);
    title('Depth'); 
    xlabel('Time[s]');
    ylabel('Depth [m]'); 
    set(gca,'Ydir','reverse');
    grid on;
    legend('Actual', 'Setpoint');
    
    subplot(4,1,2);
    plot(T_hrs, Nabla_actual, T_hrs, Nabla_command);
    title('Estimated External Oil Volume');
    grid on;
    xlabel('Time [s]');
    ylabel('Volume [mL]');
    legend('Actual', 'Setpoint');
    
    subplot(4,1,3);
    plot(T_hrs, Nabla_Scale);
    title('Scale Derived Internal Oil Volume');
    grid on;
    xlabel('Time [s]');
    ylabel('Volume [mL]');
    curr_axis = axis;
    curr_axis(3) = 0;
    axis(curr_axis);
    
    %Operating Point
    subplot(4,1,4);
    plot(T_hrs,Control_State);
    grid on;
    xlabel('Time [s]');
    %ylabel('Operating Point');
    yticks([1 2 3 4 5])
    yticklabels({'Control','Hibernate', 'Dive', 'Surface', 'Interval'});
    
%PLOT ATTITUDE
    figure; 
    plot(T_hrs, Roll, T_hrs, Pitch, T_hrs, Yaw);
    title('Attitude');
    grid on;
    xlabel('Time [s]');
    ylabel('Angle [degrees]');
    legend('Roll', 'Pitch', 'Yaw');

%PLOT YAW with Flow Rate
%     figure;
%     subplot(2,1,1);
%     plot(T_hrs, Nabla_actual);
%     grid on;
%     title('Pump Flow Rate vs. Time');
%     xlabel('Time [s]');
%     ylabel('Angle [deg]');
%     subplot(2,1,2);
%     plot(T_hrs, Yaw);
%     grid on;
%     xlabel('Time [s]');
%     ylabel('Flow Rate [mL/s]');

%PLOT Velocity Controller
    figure;
    subplot(3,1,1); 
    %plot(T_hrs, w_actual, '-k', T_hrs, z_d, '-b', T_hrs, w_command,'--r');  
    plot(T_hrs, w_actual, '-k', T_hrs, w_command,'--r');  
    ax = axis;
    if (ax(3)<-0.25)
        ax(3) = -0.25;
    end
    if (ax(4)>0.25)
        ax(4) = 0.25;
    end
    axis(ax);
    set(gca,'Ydir','reverse');
    title('Depth Rate (w)'); 
    xlabel('Time[s]');
    ylabel('Vertical Velocity [m/s]'); 
    grid on;
    legend('estimate', 'Command');
    
    %Engine Volume (Nabla_eng)
    subplot(3,1,2); 
    plot(T_hrs,Nabla_actual,'-k', T_hrs, Nabla_command,'--r'); 
    title('Volume [V]'); 
    xlabel('Time[s]');
    ylabel('\nabla [mL]'); 
    legend('Actual', 'Command');
    grid on;
    
    %Offset Adjustment
    Ki_w = -2;
    subplot(3,1,3); 
    plot(T_hrs,w_i*Ki_w ,'-k', T_hrs, Nabla_air, '-b'); 
    title('Volume Offset'); 
    xlabel('Time[s]');
    ylabel('\nabla [mL]');
    legend('offset', 'air volume');
    grid on;

%PLOT DEPTH AND OPERATING POINT
    figure; 
    %Plot Depth
    subplot(3,1,1); 
    plot(T_hrs,Depth_raw,'-k', T_hrs, z_setpoint, '--r'); 
    ax = axis;
    ax(3) = 0; %cut of at surface (z=0.0m)
    axis(ax);
    title('Depth'); 
    %xlabel('Time[hrs]');
    ylabel('Depth [m]'); 
    set(gca,'Ydir','reverse');
    grid on;
    legend('Actual', 'Setpoint');
    %Operating Point
    subplot(3,1,2);
    plot(T_hrs,Control_State);
    grid on;
    %ylabel('Operating Point');
    yticks([1 2 3 4 5])
    yticklabels({'Control','Hibernate', 'Dive', 'Surface', 'Interval'});
    %Pump State
    subplot(3,1,3);
    title('Pump State');
    plot(T_hrs,EN_PUMP);
    grid on;
    xlabel('Time [hrs]');
    curr_axis = axis;
    curr_axis(3) = -0.5;
    curr_axis(4) = 1.5;
    axis(curr_axis);
    yticks([0 1])
    yticklabels({'Off','On'});
    