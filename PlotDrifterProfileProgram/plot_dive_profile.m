function plot_dive_profile(json_filename, deploy_time)
    % Plot a notional dive profile using settings from a JSON file
    % INPUTS:
    %   json_filename: path to the JSON file with drifter settings
    %   deploy_time: (optional) deployment time to set the x-axis in terms of time
    %                otherwise, it will be in hours
    % OUTPUTS:
    %   None:plot
    
    % Read JSON file
    fid = fopen(json_filename, 'r');
    raw = fread(fid, inf);
    str = char(raw');
    fclose(fid);
    json_data = jsondecode(str);
    
    % Extract relevant data from the configurations field
    configurations = json_data.configurations;
    
    diveStartTime = NaN(1, 15);
    diveDepth = NaN(1, 15);
    diveVelocity = NaN(1, 15);
    surfaceStartTime = NaN(1, 10);
    surfaceDuration = NaN(1, 10);
    
    for i = 1:length(configurations)
        address = configurations(i).registerAddress;
        value = configurations(i).value;

        if ischar(value)
            value = str2double(value);
        end
        
        if 20 <= address && address <= 34
            diveStartTime(address - 19) = value;
        elseif 256 <= address && address <= 270
            diveDepth(address - 255) = value;
        elseif 271 <= address && address <= 285
            diveVelocity(address - 270) = value;
        elseif 35 <= address && address <= 44
            surfaceStartTime(address - 34) = value;
        elseif 45 <= address && address <= 54
            surfaceDuration(address - 44) = value;
        elseif address == 3
            preMissionTime = value; % Pre-mission timer register 3
        elseif address == 5
            abortTime = value; % Abort Time register 5
        elseif address == 60
            releaseDepth = value;
        end
    end

    % Parameters
    missionStartSetpoint = preMissionTime; % Mission starts after pre-mission time
    missionEndTimer = max(surfaceStartTime + surfaceDuration);
    dt = 1;
    t_sec = 0:dt:(missionEndTimer + preMissionTime);
    
    depth_mission = nan(1, length(t_sec));
    depth_mission(1) = 0;
    surfaceVelocity = -0.1; % guess the surface velocity
    surfIdx = 1;
    
    for tidx = 2:length(t_sec)
        current_time = t_sec(tidx);
        if current_time < preMissionTime
            depth_mission(tidx) = 0;  % pre-mission state
            continue;
        end
        
        mission_time = current_time - preMissionTime;
        diveIdx = find(mission_time >= diveStartTime & diveStartTime ~= -1, 1, 'last');
        
        if isempty(surfIdx)
            surfIdx = 1;
        end
        
        if (~isempty(diveIdx) && mission_time >= diveStartTime(diveIdx)) && ...
               (~(mission_time >= surfaceStartTime(surfIdx)) || surfaceStartTime(surfIdx) == -1)
            if depth_mission(tidx - 1) < diveDepth(diveIdx)
                depth_mission(tidx) = depth_mission(tidx - 1) + diveVelocity(diveIdx) * dt;
            else
                depth_mission(tidx) = diveDepth(diveIdx);
            end
        elseif mission_time >= surfaceStartTime(surfIdx) && surfaceStartTime(surfIdx) ~= -1
            surfTime = surfaceStartTime(surfIdx) + surfaceDuration(surfIdx);
            if depth_mission(tidx - 1) > 0
                depth_mission(tidx) = depth_mission(tidx - 1) + surfaceVelocity * dt;
            elseif depth_mission(tidx - 1) <= 0 && mission_time < surfTime
                depth_mission(tidx) = 0;
            elseif mission_time >= surfTime && depth_mission(tidx - 1) <= 0
                surfIdx = surfIdx + 1;
                depth_mission(tidx) = 0;
            end
        end
    end
    
    % Plot
    if nargin > 1
        t = deploy_time + seconds(t_sec);
        plot(t, depth_mission, 'linewidth', 2);
        hold on;
        plot(t, releaseDepth * ones(size(t)), '--r', 'linewidth', 2);
        
        % Add vertical line for abort time
        abortTime_datetime = deploy_time + seconds(abortTime + preMissionTime);
        xline(abortTime_datetime, 'r', 'LineWidth', 2, 'Label', 'Abort Time');
        
        % Add vertical line for mission start time
        missionStartTime_datetime = deploy_time + seconds(preMissionTime);
        xline(missionStartTime_datetime, 'g', 'LineWidth', 2, 'Label', 'Mission Start Time');
        
        grid on; grid minor;
        xlabel('Time');
        ylabel('Depth, m');
        dx = hours(2);
        ax2 = gca();
        ax2.XTick = t(1):dx:t(end);
        set(gca, 'XTickLabelRotation', 90);
        datetick('x', 'mm-dd, HH:MM:SS', 'keepticks');
        title('Dive Profile');
    else
        t = t_sec / 3600;
        plot(t, depth_mission, 'linewidth', 2);
        hold on;
        plot(t, releaseDepth * ones(size(t)), '--r', 'linewidth', 2);
        
        % Add vertical line for abort time
        xline((abortTime + preMissionTime) / 3600, 'r', 'LineWidth', 2, 'Label', 'Abort Time');
        
        % Add vertical line for mission start time
        xline(preMissionTime / 3600, 'g', 'LineWidth', 2, 'Label', 'Mission Start Time');
        
        xlabel('Hours');
        grid on; grid minor;
        ylabel('Depth, m');
        title('Dive Profile');
    end
    
    set(gca, 'YDir','reverse') ;
    set(gca, 'fontweight', 'bold', 'fontsize', 14);
    xlim([t(1) t(end)]);
    legend('Dive Profile', 'Release Depth', 'Abort Time', 'Mission Start Time');
end
