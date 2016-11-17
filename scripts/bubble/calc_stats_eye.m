function calc_stats_eye( eyeImages )
%CALC_STATS_EYE Summary of this function goes here
%   Detailed explanation goes here

    nfiles = length(eyeImages);
    
    allFixations = [];
    allTimes  = [];
    groups    = [];
    for i = 1:nfiles
        % Clicks
        fixPerImage = []; 
        for j = 1:length(eyeImages(i).userdata)
            if ~isempty(eyeImages(i).userdata(j).fixations) && ...
                ~isempty(eyeImages(i).userdata(j).fixations.enc)
                fixPerUser = length(eyeImages(i).userdata(j).fixations.enc);
                fixPerImage = [fixPerImage; fixPerUser];
                groups    = [groups; i];
            end
        end

        fprintf('Fix = Image %d (Avg: %.2f, Median: %.2f, Max=%.2f, Min=%.2f, SD=%.2f)\n',i, ...
            mean(fixPerImage), median(fixPerImage),...
            max(fixPerImage), min(fixPerImage), std(fixPerImage));
        allFixations = [allFixations; fixPerImage];
        
        % Timespan
        timesPerImage = []; 
        for j = 1:length(eyeImages(i).userdata)
            if ~isempty(eyeImages(i).userdata(j).fix_durations) && ...
                ~isempty(eyeImages(i).userdata(j).fix_durations.enc)
            
                elapsed = sum(eyeImages(i).userdata(j).fix_durations.enc)/1000;
                timesPerImage = [timesPerImage; elapsed/60];
            end
        end
        
        fprintf('Time = Image %d (Avg: %.2f, Median: %.2f, Max=%.2f, Min=%.2f, SD=%.2f)\n\n',i, ...
            mean(timesPerImage), median(timesPerImage), ...
            max(timesPerImage), min(timesPerImage), std(timesPerImage));
        allTimes = [allTimes; timesPerImage];        
    end
    fprintf('Total.Avg.Fix: %.2f, Total.Med.Fix: %.2f, (SD=%.2f)\n',...
        mean(allFixations), median(allFixations), std(allFixations));
    fprintf('Total.Avg.Time: %.2f, Total.Med.Time: %.2f, (SD=%.2f)\n',...
        mean(allTimes), median(allTimes), std(allTimes));
    
    figure(1), boxplot(allFixations,groups);
    figure(2), boxplot(allTimes,groups);
    fprintf('click vs time correlation = %.2f\n', CC(allFixations, allTimes));

end

