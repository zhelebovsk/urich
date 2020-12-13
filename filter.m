clear, clc
IM = imread('HK.jpg');
IM = IM(:,:,1);

noise = 1/159*[2 4  5  4  2;
               4 9  12 9  4;
               5 12 15 12 5;
               4 9  12 9  4;
               2 4  5  4  2];
F = uint8(filter2(noise,IM));
mat = [1 2 1; 0 0 0; -1 -2 -1];
H = uint32(filter2(mat,F));
V = uint32(filter2(mat',F));
SOB = (H.*H + V.*V);
SOB = uint8(sqrt(double(SOB)));
ORIENT = rad2deg(atan(double(SOB)));
H = uint8(H);
V = uint8(V);
figure(1)
subplot(2,2,1)
imshow(IM)
subplot(2,2,2)
imshow(SOB)
subplot(2,2,3)
imshow(H)
subplot(2,2,4)
imshow(V)
