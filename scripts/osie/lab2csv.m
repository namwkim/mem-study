
images = dir('./bubble-images/*.jpg');
fid=fopen('lab-clicks.csv','wt');
for i=1:length(images)
    [pathstr,name,ext] = fileparts(images(i).name);
    load(strcat('./data/mouse_lab/', name, '.mat'));
    name
    for j=1:length(fixations.subj)
        x = 0.8*fixations.coord(j,2);
        y = 0.8*fixations.coord(j,1);
        t = fixations.order(j);
        k = fixations.subj(j);
        fprintf(fid,'%d, %s, %d, %f, %f\n', t, char(images(i).name), k, x, y);
    end
end

