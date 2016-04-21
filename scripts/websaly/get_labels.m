mixed= dir('./images/mixed/*.png');
text= dir('./images/text/*.png');
pictorial= dir('./images/pictorial/*.png');

images= dir('./targets_websaly/*.png');
fid=fopen('websaly-image-labels.csv','wt');
for i=1:length(images)
    for j=1:length(mixed)
        if strcmp(mixed(j).name, images(i).name)
            fprintf(fid,'%s, %s\n', images(i).name, 'mixed');
            continue
        end
    end
    for j=1:length(text)
        if strcmp(text(j).name, images(i).name)
            fprintf(fid,'%s, %s\n', images(i).name, 'text');
            continue
        end
    end
    for j=1:length(pictorial)
        if strcmp(pictorial(j).name, images(i).name)
            fprintf(fid,'%s, %s\n', images(i).name, 'pictorial');
            continue
        end
    end
end
% 
% % sample 17 images from each category
% ind = randsample(length(mixed), 17);
% sample_mixed = mixed(ind);
% ind = randsample(length(text), 17);
% sample_text = text(ind);
% ind = randsample(length(pictorial), 17);
% sample_pictorial = pictorial(ind);
% 
% all = [sample_mixed; sample_text; sample_pictorial];
% 
% savepath = './images/targets';
% if exist(savepath, 'dir')
%     rmdir(savepath,'s');
% end
% mkdir(savepath);
% 
% for i=1:length(all)
%     image = all(i);
%     imgpath = sprintf('./images/all/%s', image.name);
%     im = imread(imgpath);
%     imgpath = sprintf('./images/targets/%s', image.name);
%     imwrite(im, imgpath);
% end