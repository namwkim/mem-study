
% load all images
images = dir('../../bubble-db-pilot/targets/*.png');
% image = 'practice';
radi = 40;
blur_dir = '../../bubble-db-pilot/targets_blurred';
if exist(blur_dir, 'dir')
    rmdir(blur_dir,'s');
end
mkdir(blur_dir);
H = fspecial('gaussian',radi,radi); 

% read image
for j=1:length(images)
    imgpath = sprintf('../../bubble-db-pilot/targets/%s', images(j).name);
    im = imread(imgpath);
    blurim = imfilter(im,H,'replicate');
    imgpath = sprintf('./%s/%s', blur_dir, images(j).name);
    imwrite(blurim, imgpath);
end
