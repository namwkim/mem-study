
% load all images
images = dir('./images/targets/*.jpg');
ws = [];
hs = [];
% read image
for j=1:length(images)
    imgpath = sprintf('./images/targets/%s', images(j).name)
    im = imread(imgpath);
    [w, h, k] = size(im);
    ws = [ws;w];
    hs = [hs;h];
end
max(ws)
max(hs)