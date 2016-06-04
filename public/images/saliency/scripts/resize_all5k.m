% load all images
loadpath = '../../all5k'
all5k= dir(strcat(loadpath, '/*.png'));
% mkdir to which resized files are copied
savepath = '../../temp_dir';
if exist(savepath, 'dir')
    rmdir(savepath,'s');
end
mkdir(savepath);
% for each image, resize
maxH = 600;
maxW = 600;
for i=1:length(all5k)
    image = all5k(i);
    imgpath = sprintf(strcat(loadpath, '/%s'), image.name);
    imgpath
    [im, map]  = imread(imgpath);
    % resize 
    [H, W, D] = size(im);
    ratio = min(maxW/W, maxH/H);  
    if ratio>1.0
        imr = im;
    else
        if isempty(map)
            imr = imresize(im, ratio);
        else
            [imr, map] = imresize(im, map, ratio);
        end
    end
    imgpath = sprintf(strcat(savepath, '/%s'), image.name);
    if isempty(map)
        imwrite(imr, imgpath);
    else
        imwrite(imr, map, imgpath);
    end
end