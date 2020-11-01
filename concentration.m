clear
clc
myFolder = 'C:\Py code\particle proc\2'
filePattern = fullfile(myFolder, '*.bmp');
jpegFiles = dir(filePattern);
mat = uint8(zeros(600,1920,length(jpegFiles)));
for k = 1:length(jpegFiles)
  baseFileName = jpegFiles(k).name;
  fullFileName = fullfile(myFolder, baseFileName);
  fprintf(1, 'Now reading %s\n', fullFileName);
  imageArray = imread(fullFileName);
  %imshow(imageArray);  % Display image.
  drawnow; % Force display to update immediately.
  mat(:,:,k) = imageArray(201:800,1:1920);
end
%наложть маску
mask = uint8(ones(size(mat(:,:,1))));
mask(230:380, 1485:end) = 0;
mask(220:396, 1370:1485) = 0;
for i = 200:450
    for j = 1200:1500
        if (i - 308)^2 + (j - 1370)^2 < 88^2
            mask(i,j) = 0;
        end
    end
end
for i = 1:k
    mat(:,:,i) = mat(:,:,i).* mask(:,:);
end

%определяются минимальные значения каждого пикселя по всем кадрам и
%вычитаются из считанных данных
M = min(mat,[],3);
mat = mat - M;
%трешхолд и бинаризация данных
BW = mat;
BW(BW<20) = 0;
BW(BW>1) = 255;

%определение среднего значения каждого пикселя по всем кадрам, трешхолд
M1 = mean(BW,3);
T = M1;
T(T>8)=8
%осреднение и вывод контуров концентраций 
K = (1/900)*ones(30);
Ts = conv2(T,K,'same');
G = fspecial('gaussian',[5 5],2);
Af = filter2(G,A,'same');
