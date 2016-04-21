load('./data/eye/fixations.mat');

images = dir('./bubble-images/*.jpg');
fid=fopen('eye-clicks.csv','wt');
for i=1:length(images)
    for j=1:length(fixations)
        
        if strcmp(fixations{j}.img, images(i).name)==1
            images(i).name
            for k=1:length(fixations{j}.subjects)
                for z=1:length(fixations{j}.subjects{k}.fix_x)
                    x = 0.8*fixations{j}.subjects{k}.fix_x(z);
                    y = 0.8*fixations{j}.subjects{k}.fix_y(z);
                    t = fixations{j}.subjects{k}.fix_duration(z);
                    fprintf(fid,'%d, %s, %d, %f, %f\n', t, char(fixations{j}.img), k, x, y);
                end
            end
        end            
    end
end