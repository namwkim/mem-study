% load all images
loadpath = './all5k-reduced'
all5k= dir(strcat(loadpath, '/*.png'));
% mkdir to which resized files are copied
savepath = './all5k';
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
    im  = imread(imgpath);
    % resize 
    [H, W, D] = size(im);
    ratio = min(maxW/W, maxH/H);  
    if ratio>1.0
        imr = im;
    else
        imr = imresize(im, ratio);
    end
    imgpath = sprintf(strcat(savepath, '/%s'), image.name);
    imwrite(imr, imgpath);
end