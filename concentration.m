clear all
clc
tic
%% working dir and file format
% S - data of each image
D  = 'C:\Users\Dantec-PIV\Desktop\HS-V images\Dust test\matlab\raw';
Ds = 'C:\Users\Dantec-PIV\Desktop\HS-V images\Dust test\matlab\substructed background';
Dt = 'C:\Users\Dantec-PIV\Desktop\HS-V images\Dust test\matlab\threshold';
De = 'C:\Users\Dantec-PIV\Desktop\HS-V images\Dust test\matlab\edges';
if ~isfolder(D)
    errorMessage = sprintf('Error: The following folder does not exist:\n%s', D);
    uiwait(warndlg(errorMessage));
    return
end
FolderCheck(Ds)
FolderCheck(Dt)
FolderCheck(De)
S = dir(fullfile(D, '*.bmp'));
disp('Folders are OK')
toc
disp('---------------------')
%% fps, dt, mm/px
if isfile(fullfile(D, 'info.txt'))
    fid = fopen(fullfile(D, 'info.txt'), 'r');
    [~] = fgetl(fid);
    fps = fgetl(fid);
    fps = regexprep(fps, 'ГЉГ Г¤Г°Г®Гў Гў Г±ГҐГЄГіГ­Г¤Гі: ', '');
    fps = str2double(fps);
    dt = 1/fps;
    [~] = fclose(fid);
    disp('Info.txt has been read')
    toc
    disp('---------------------')
else
    dt  = NaN;
    warning('No info.txt')
    toc
    disp('---------------------')
end
mmpx = 17.0/226.0; %mm/px
%% file names
for i = 1:numel(S)
    S(i).fname = char(fullfile(S(i).folder,S(i).name));
    S(i).subsfilename = char(fullfile(Ds, [int2str(i) '.bmp']));
    S(i).thresholdfilename = char(fullfile(Dt, [int2str(i) '.bmp']));
    S(i).edgefilename = char(fullfile(De, [int2str(i) '.bmp']));
    S(i).time = dt * (i - 1);
end
S = rmfield(S, {'bytes', 'isdir', 'datenum', 'folder', 'name'});
%% crop
crop = true;
if crop
    a = 1; 
    c = 921; 
    b = 304; 
    d = 1920; 
    D = 'C:\Users\Dantec-PIV\Desktop\HS-V images\Dust test\matlab\rawCrop'; %#ok<UNRCH>
    FolderCheck(D)
    for i = 1:numel(S)
        raw = imread(S(i).fname);
        raw = raw(a:b, c:d);
        S(i).fname = char(fullfile(D, [int2str(i) '.bmp']));
        imwrite(raw, S(i).fname)
    end
    disp('Crop is done')
    toc
    disp('---------------------')
end
clear i D Ds Dt De dt fid f a b c d crop
%% background
[S(1).res(1), S(1).res(2)] = size(imread(S(1).fname));
rawMin = 255 * uint8(ones(S(1).res(1), S(1).res(2)));
for i = 1:numel(S)
    raw = imread(S(i).fname);
    rawMin = min(raw, rawMin);
    [S(i).res(1), S(i).res(2)] = size(raw);
    imwrite(raw, S(i).subsfilename)
end
clear i raw
imwrite(rawMin,'background.bmp')
disp('Background has been found')
toc
disp('---------------------')
%% processing
se = strel('disk',1); 
for i = 1:numel(S)
    %background subs
    raw = imread(S(i).fname) - rawMin;
    imwrite(raw, S(i).subsfilename)
    %threshold
    raw(raw < 1) = 0;
    imwrite(raw, S(i).thresholdfilename)
    %edge
    raw = 255 * uint8(edge(raw,'log'));
    raw = imfill(raw, 'holes');
    raw = imopen(raw,se);
    imwrite(raw, S(i).edgefilename)
    [~, L] = bwboundaries(raw);
    %particle params
    param = regionprops(L, 'Centroid', 'EquivDiameter', 'Area', 'Circularity', 'BoundingBox', 'Image', 'Orientation');
    [~,index] = sortrows([param.Area].'); 
    param = param(index(end:-1:1));
    S(i).partparams = param;
end
clear i raw param L index se
disp('Edges have been found')
toc
disp('---------------------')
for i = 1:numel(S)
    raw = imread(S(i).subsfilename);
    for j = 1:numel(S(i).partparams)
        x1 = uint16(S(i).partparams(j).BoundingBox(1));
        y1 = uint16(S(i).partparams(j).BoundingBox(2));
        x2 = x1 + uint16(S(i).partparams(j).BoundingBox(3)) - 1;
        y2 = y1 + uint16(S(i).partparams(j).BoundingBox(4)) - 1;
        S(i).partparams(j).imagegrey = raw(y1:y2,x1:x2);
        S(i).partparams(j).mmArea = mmpx * mmpx * S(i).partparams(j).Area;
        S(i).partparams(j).mmEquivDiameter = mmpx * S(i).partparams(j).EquivDiameter;
    end
end
clear x1 x2 y1 y2 raw i j 
%% plots
n = 3; % num of image to show
subplot(5,2,1)
imshow(imread(S(n).fname))
title('RAW image')
subplot(5,2,2)
imshow(rawMin)
title('Background (rawMin)')
subplot(5,2,3)
imshow(imread(S(n).subsfilename))
title('Substructed background')
subplot(5,2,4)
imshow(S(n).thresholdfilename)
title('Threshold (I)')
subplot(5,2,5)
imshow(S(n).edgefilename)
title('Edges of particles (E)')
subplot(5,2,6)
imshow(imread(S(n).fname))
title('Centroids')
hold on
for i = 1:numel(S(n).partparams)
    x1 = uint16(S(n).partparams(i).BoundingBox(1));
    y1 = uint16(S(n).partparams(i).BoundingBox(2));
    x2 = x1 + uint16(S(n).partparams(i).BoundingBox(3)) - 1;
    y2 = y1 + uint16(S(n).partparams(i).BoundingBox(4)) - 1;
    plot([x1 x1 x2 x2 x1],[y1 y2 y2 y1 y1])
    plot(S(n).partparams(i).Centroid(1), S(n).partparams(i).Centroid(2),'r+')
end
%%
%figure()
%hold on
%for i = 1:numel(S)
%    imshow(imread(S(i).fname))
%    hold on
%    for j = 1:numel(S(i).partparams)
%        plot(S(i).partparams(j).Centroid(1), S(i).partparams(j).Centroid(2),'r+')
%    end
%    pause(0.1)
    %x1 = uint16(S(n).partparams(i).BoundingBox(1));
    %y1 = uint16(S(n).partparams(i).BoundingBox(2));
    %x2 = x1 + uint16(S(n).partparams(i).BoundingBox(3)) - 1;
    %y2 = y1 + uint16(S(n).partparams(i).BoundingBox(4)) - 1;
    %plot([x1 x1 x2 x2 x1],[y1 y2 y2 y1 y1])
    %plot(S(n).partparams(i).Centroid(1), S(n).partparams(i).Centroid(2),'r+')
%end
clear x1 x2 y1 y2
clear i 
%%
nvdiv = 20;
VerticalDistribution = (zeros(nvdiv, 1));
for i = 1:numel(S)
    a = (zeros(nvdiv, 1));
    for j = 1:numel(S(i).partparams)
        t = fix((S(i).partparams(j).Centroid(1) - 1) / (S(i).res(2)/nvdiv)) + 1;
        a(t) = a(t) + 1;
    end
    S(i).VerticalDistribution = a;
    VerticalDistribution = VerticalDistribution + a;
end
VerticalDistribution = VerticalDistribution./numel(S);
clear t i j a nvdiv
subplot(5,2,7)
plot(VerticalDistribution)

%%
nhdiv = 20;
HorizontalDistribution = (zeros(nhdiv, 1));
for i = 1:numel(S)
    a = (zeros(nhdiv, 1));
    for j = 1:numel(S(i).partparams)
        t = fix((S(i).partparams(j).Centroid(2) - 1) / (S(i).res(1)/nhdiv)) + 1;
        a(t) = a(t) + 1;
    end
    S(i).HorizontalDistribution = a;
    HorizontalDistribution = HorizontalDistribution + a;
end
HorizontalDistribution = HorizontalDistribution./numel(S);
clear t i j a nhdiv
subplot(5,2,8)
plot(HorizontalDistribution)
%%
nhdiv = 10;
nvdiv = 20;
Distribution = (zeros(nhdiv, nvdiv));
for i = 1:numel(S)
    a = (zeros(nhdiv, nvdiv));
    for j = 1:numel(S(i).partparams)
        t = fix((S(i).partparams(j).Centroid(2) - 1) / (S(i).res(1)/nhdiv)) + 1;
        w = fix((S(i).partparams(j).Centroid(1) - 1) / (S(i).res(2)/nvdiv)) + 1;
        a(t, w) = a(t, w) + 1;
    end
    S(i).Distribution = a;
    Distribution = Distribution + a;
end
Distribution = Distribution./numel(S);
clear t i j a nhdiv
subplot(5,2,9)
imagesc(Distribution)





function [] = FolderCheck(D)
    if ~isfolder(D)
        mkdir(D)
    else
        rmdir(D, 's')
        mkdir(D)
    end
end
