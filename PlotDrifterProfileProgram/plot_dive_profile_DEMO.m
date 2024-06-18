%cfg_filename = 'drifter.cfg';
cfg_filename = 'Bounce_Profile.cfg'

% Example deploy time: May 24, 2024, 10:00 AM
magnet_time = datetime(2024, 5, 24, 10, 0, 0); 

% Call the function to plot the dive profile
plot_dive_profile(cfg_filename, magnet_time);
