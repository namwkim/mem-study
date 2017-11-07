
homedir = './'

a=['EF0000';'FF6000';'FFCF00';'BFFF40';'50FFAF';'00DFFF';'0090FF';'0040FF';'0000FF';'0000AA']

col=[hex2dec(a(:,1:2)) hex2dec(a(:,3:4)) hex2dec(a(:,5:6))];

imageDir=[homedir,'../../public/images/annotate/']; %design/images/gd_small/'];

outputDir=[homedir,'design/textlabel/gd2_5_textsize/']
mkdir(outputDir);


checkDir=[homedir,'design/textlabel/gd2_5_worker/']
mkdir(checkDir);


resultsFile=[homedir,'annotate-sample.csv']

fid=fopen(resultsFile,'r');

% Changes by Nam: File path, and wrong argument order for strsplit (maybe
% it is a version issue)

checkIds={};
reject={};

tline = fgets(fid);
tline = fgets(fid);
i = 0
while ischar(tline)
    %disp(tline)
    
    close all
    i = i+1
%     splt=strsplit(',',tline);
    
    r=regexp(tline,',','split');
    workerId=strrep(r{5},'"','')
    hitId=strrep(r{1},'"','')
    

    images=strfind(tline,'../../images/annotate');
    
    numLinesList=[];
    markedImages=0;
    
    for i=1:length(images)
        
        
        startIdx=max(strfind(tline(1:images(i)),'"'));
        a=strfind(tline,'"');
        endIdx=min(a(a>startIdx));
        
        strokeStr=tline(startIdx+1:endIdx-1);
        strsplit(strokeStr,':')
        strokeSplit=strsplit(strokeStr,':')
        
        strokeInfo=strsplit(strokeSplit{1},',');
       
        w=str2num(strokeInfo{1});
        h=str2num(strokeInfo{2});
        fname=strokeInfo{3};
        
        fname=fname(max(strfind(fname,'/'))+1:length(fname));
        
        
        if ~isempty(strfind(fname,'practice'))
            continue
        end
        
        img=double(imread([imageDir,fname]));


        userDrawnMap=zeros(h,w);
        userSizeMap=zeros(h,w);
        userRelSizeMap=zeros(h,w);
        
        strokes=strsplit(strokeSplit{2},';');
        
        [xpts,ypts] = meshgrid(1:w, 1:h);
        
        drawn=0;
       % strokes

        
        for s=1:length(strokes)-1
            %strokes{s}
            strk=strsplit(strokes{s},',');
            type=str2num(strk{2});
            numLines=str2num(strk{3});
            
            numLinesList=[numLinesList numLines];
            
            if length(strk)<10 
                shortProb=strk
                err=1;
                continue
            end
            
            if rem((length(strk)-4)/2,1)>0
                remProb=strk
                 err=1;
                 continue
            end
            
            drawn=1;
            
            if (type==3)
                x1=min(max(round(str2num(strk{4}))-10,1),w);
                y1=min(max(round(str2num(strk{5}))-10,1),h);
              
                
                xn=min(max(round(str2num(strk{length(strk)-2}))-10,1),w);
                yn=min(max(round(str2num(strk{length(strk)-1}))-10,1),h);
                
                if yn < y1
                   tmp=yn;
                   yn=y1;
                   y1=tmp;
                end
                
                if xn < x1
                   tmp=xn;
                   xn=x1;
                   x1=tmp;
                end
                
                userDrawnMap(y1:yn,x1:xn)=numLines;
                userSizeMap(y1:yn,x1:xn)=min((yn-y1),(xn-x1))./numLines;
                
                userRelSizeMap(y1:yn,x1:xn)=min((yn-y1)/h,(xn-x1)/w)./numLines;
                
                
                
            elseif (type==4)
               
                numPts=(length(strk)-4)/2;
                pts=zeros(numPts,2);
                for j=1:numPts
                    pts(j,1)=str2num(strk{3+j*2-1})-10;
                    pts(j,2)=str2num(strk{3+j*2})-10;
                end
                
                inside = inpolygon(xpts,ypts,pts(:,1),pts(:,2));
                
                vert=sum(double(inside));
                horiz=sum(double(inside),2);
                
                vmed=median(vert(vert>0));
                hmed=median(horiz(horiz>0));
                
                userDrawnMap(inside>0)=numLines;
                userSizeMap(inside>0)= min(vmed,hmed)./numLines;
                
                userRelSizeMap(inside>0)=min(vmed/h,hmed/w)./numLines;
            else
                typeerror=type
            end
        
        end
        if drawn==1
           markedImages=markedImages+1;
            
       
            save([outputDir,fname(1:length(fname)-4),'_',workerId],'userDrawnMap','userSizeMap','userRelSizeMap','strokes');
           
           
            %imwrite(uint8(userMap), [outputDir,fname(1:length(fname)-4),'_',workerId,'.png'])
            
            
 

            userMapR=zeros(h, w);
            userMapG=zeros(h, w);
            userMapB=zeros(h, w);

            for c=1:10
                userMapR(userDrawnMap==c)=col(c,1);
                userMapG(userDrawnMap==c)=col(c,2);
                userMapB(userDrawnMap==c)=col(c,3);
            end
            clear userMapCol
            userMapCol(:,:,1)=userMapR;
            userMapCol(:,:,2)=userMapG;
            userMapCol(:,:,3)=userMapB;

            userMapCol=imresize(userMapCol, [size(img,1), size(img,2)]);

            f=figure(1);clf;
            subaxis(2,2,1);
            imshow(img./255);



            greyImg=rgb2gray(img./255);
            clear greyImg3
            greyImg3(:,:,1)=greyImg;
            greyImg3(:,:,2)=greyImg;
            greyImg3(:,:,3)=greyImg;

            imgDisp=255*greyImg3 + 0.6*userMapCol;
            imgDisp(imgDisp>255)=255;
             subaxis(2,2,2);
            imshow(imgDisp./255);
            
            

            imgDisp=userMapCol;
            imgDisp(imgDisp>255)=255;
            subaxis(2,2,3);
            imshow(imgDisp./255);

            
            imgDisp=4*userRelSizeMap;
            subaxis(2,2,4);
            imshow(imgDisp);

            saveas(f,[checkDir,hitId,'-',fname(1:length(fname)-4),'_',workerId,'.png'])
           
        end
        
    end
    
    if (var(numLinesList) < 0.5)
        checkIds{length(checkIds)+1}=workerId;
    end
    
    if markedImages < 10
       reject{1,size(reject,2)+1}=hitId;
       reject{2,size(reject,2)}=workerId;
       reject{3,size(reject,2)}=['Only ',markedImages,' images have been finished'];
       
    end
    
    
    tline = fgets(fid);
end

fclose(fid);




textDir=[homedir,'design/textlabel/gd2_5_textsize/']


imgList=dir(textDir)


images={};
for i=3:length(imgList)
    
    if imgList(i).isdir
        continue
    end
    
    fname=strrep(imgList(i).name,'_A','-A');
    splt=strsplit('-',fname);
    
   if (isempty(find(ismember(images, splt{1})==1)))
       images{length(images)+1}=splt{1};
   end  
end


workerIds={};
order=zeros(1,100);
cnt=zeros(1,100);
dists=zeros(1,100);

for i=1:length(images)
    
    
    flist=dir([textDir,images{i},'*']);
    
    avgMap=[];
    for j=1:length(flist)
        
        load([textDir,flist(j).name])
        
        if length(avgMap)==0
            avgMap=userSizeMap;
        else
            avgMap=avgMap+imresize(userSizeMap, [size(avgMap,1) size(avgMap,2)]);
        end
    end
    
    avgMap=avgMap./length(flist);
    
    dist=zeros(length(flist),1);
    
    checkPixels=avgMap>0;
    
    imgWorkerIds={};
    
    for j=1:length(flist)
        load([textDir,flist(j).name])
        
        fname=strrep(flist(j).name,'_A','-A');
        workerId=fname(strfind(fname,'-')+1:strfind(fname,'.')-1);

       diff=abs(avgMap-imresize(userSizeMap, [size(avgMap,1) size(avgMap,2)]));
       dist(j)=mean(diff(checkPixels));
       imgWorkerIds{j}=workerId;
        

    end
    
    [a idx]=sort(dist);
    
    for j=1:length(a)
    
       workerId=imgWorkerIds{idx(j)};
       wId= find(ismember(workerIds, workerId)==1);
       if (isempty(wId))
           workerIds{length(workerIds)+1}=workerId;
           wId= find(ismember(workerIds, workerId)==1);
       end 
        order(wId)=order(wId)+j/length(a);
        cnt(wId)=cnt(wId)+1;
        dists(wId)=dists(wId)+a(j);

    end

      % order(wId)=currDist;

end

order(cnt==0)=[];
dists(cnt==0)=[];
cnt(cnt==0)=[];

[worst idx]= sort(order./cnt, 'descend')


for i=1:length(idx)
    workerIds{idx(i)}
end

length(idx)
% commented by Nam
% for i=1:30
%     fprintf('%s\n', workerIds{idx(i)})
% end







