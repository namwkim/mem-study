% save target images as 0.8 scaled down images. 

images = dir('./images/targets/*.jpg');
mkdir('./targets_osie');
for i=1:length(images)
    image = images(i);
    imgpath = sprintf('./images/targets/%s', image.name);
    im = imread(imgpath);
    resized = imresize(im, 0.8);
    imgpath = sprintf('./targets_osie/%s',  image.name);
    imwrite(resized, imgpath);
end