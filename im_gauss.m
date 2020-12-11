clear, clc
im = imread('Palo_Duro_Lighthouse.jpg');
R = im(:,:,1);
G = im(:,:,2);
B = im(:,:,3);
figure(1)
subplot(3,3,1)
imshow(im)
title('Original')
subplot(3,3,4)
imshow(R)
title('R')
subplot(3,3,5)
imshow(G)
title('G')
subplot(3,3,6)
imshow(B)
title('B')
subplot(3,3,2)
imshow(R)
title('input')
%subplot(3,3,8)
fftR = fft2(R);
sfftR = fftshift(fftR);
cy = size(R,1);
cx = size(R,2);
proc = 0.5;
for i = 1:size(R,1)
    for j = 1:size(R,2)
        EL(i,j) = exp(-((i-cy/2)/(cy/2*proc))^2 -((j-cx/2)/(cx/2*proc))^2);
        % круг в центре
        %if (((i-size(R,1)/2)/(size(R,1)/2*proc))^2 + ((j-size(R,2)/2)/(size(R,2)/2*proc))^2 < 1)
        %    EL(i,j) = 1;
        %else
        %    EL(i,j) = 0;
        %end
    end
end

subplot(3,3,7)
imshow(log(abs(EL)+1))


subplot(3,3,8)
imagesc(log(abs(sfftR)+1))
title('shft fft input')

subplot(3,3,9)
sfftR = sfftR .* EL;
imagesc(log(abs(sfftR)+1))
title('sfftR')

invsfftR = ifftshift(sfftR);
modR = uint8(ifft2(invsfftR));

subplot(3,3,3)
imshow(real(modR))
title('output')


