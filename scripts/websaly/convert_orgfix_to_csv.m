
load('original_fixations.mat');
load('websaly10x70.mat')

%  curTime = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
%             csvwriter.writerow([curTime, imgName, workderID, coord[1], coord[0]])

csvdata = [];
fid=fopen('websaly-clicks.csv','wt');
for i=1:length(fixations)
    
    for j=1:length(bubble)
        if strcmp(fixations{i}.img,bubble(j).filename)==1
            for k=1:length(fixations{i}.subjects)
%                 subject = fixations{i}.subjects{k}
                for l=1:length(subject.fix_x)
                    fprintf(fid,'%d, %s, %d, %f, %f\n', subject.fix_time(l), char(fixations{i}.img), k, subject.fix_x(l), subject.fix_y(l));
                end
            end
        end
    end
end