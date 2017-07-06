
% load all images
numBatches = 7;
for i=1:numBatches
    i
    images = dir(sprintf('../batch-%d/*.png', i));
    target_dir = sprintf('../batch-%d-blurred', i);
    mkdir(target_dir);


    H = fspecial('gaussian',40, 40); 


    for j=1:length(images)
        imgpath = sprintf('../batch-%d/%s', i, images(j).name);
        [im, map] = imread(imgpath);
        if isempty(map)==false
            im = ind2rgb(im,map);
        end        
        blurim = imfilter(im,H,'replicate');
        imgpath = sprintf('%s/%s', target_dir, images(j).name);
        imwrite(blurim, imgpath);
        if isempty(map)
            
        else
            imwrite(blurim, map, imgpath);
        end
    end
end    
% blur 
% save image