
% load all images
images = dir('./targets/*.jpg');

mkdir('targets_blurred')

H = fspecial('gaussian',40,40); 

% read image
for i=1:length(images)
    imgpath = sprintf('./targets/%s', images(i).name);
    im = imread(imgpath);
    blurim = imfilter(im,H,'replicate');
    imgpath = sprintf('./targets_blurred/%s', images(i).name);
    imwrite(blurim, imgpath);
end

    
% blur 
% save image