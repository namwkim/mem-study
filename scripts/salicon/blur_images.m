
% load all images
% images = dir('./targets/*.jpg');
image = 'salicon-practice';
radi = [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80];
for i=1:length(radi)
%     blur_dir = sprintf('targets_blurred_%d', radi(i));
%     mkdir(blur_dir)

    H = fspecial('gaussian',radi(i),radi(i)); 

    % read image
%     for j=1:length(images)
%         imgpath = sprintf('./targets/%s', images(j).name);
%         im = imread(imgpath);
%         blurim = imfilter(im,H,'replicate');
%         imgpath = sprintf('./%s/%s', blur_dir, images(j).name);
%         imwrite(blurim, imgpath);
%     end
    imgpath = sprintf('./%s.jpg', image);
    im = imread(imgpath);
    blurim = imfilter(im,H,'replicate');
    imgpath = sprintf('./%s-blurred_%d.jpg',  image, radi(i));
    imwrite(blurim, imgpath);
end
    
% blur 
% save image