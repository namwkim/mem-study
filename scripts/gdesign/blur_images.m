
% load all images
images = dir('./images/targets/*.jpg');
% image = 'practice';
radi = [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80];
for i=1:length(radi)
    blur_dir = sprintf('./images/targets_blurred_%d', radi(i));
    if exist(blur_dir, 'dir')
        rmdir(blur_dir,'s');
    end
    mkdir(blur_dir);
    H = fspecial('gaussian',radi(i),radi(i)); 

    % read image
    for j=1:length(images)
        imgpath = sprintf('./images/targets/%s', images(j).name);
        im = imread(imgpath);
        blurim = imfilter(im,H,'replicate');
        imgpath = sprintf('./%s/%s', blur_dir, images(j).name);
        imwrite(blurim, imgpath);
    end
%     imgpath = sprintf('./images/%s.jpg', image);
%     im = imread(imgpath);
%     blurim = imfilter(im,H,'replicate');
%     imgpath = sprintf('./images/%s-blurred_%d.jpg',  image, radi(i));
%     imwrite(blurim, imgpath);
end