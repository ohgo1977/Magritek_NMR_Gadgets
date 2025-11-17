%  ------------------------------------------------------------------------
%  File Name   : magritek2d2mat.m
%  Description : MATLAB function to convert Magritek binary 2D data (data.2d) to MATLAB data
%  Developer   : Dr. Kosuke Ohgo
%  ULR         : https://github.com/ohgo1977/Magritek_NMR_Gadgets
%  Version     : 1.0.0
%  ------------------------------------------------------------------------
%
% MIT License
%
% Copyright (c) 2023 Kosuke Ohgo
%
% Permission is hereby granted, free of charge, to any person obtaining a copy
% of this software and associated documentation files (the "Software"), to deal
% in the Software without restriction, including without limitation the rights
% to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
% copies of the Software, and to permit persons to whom the Software is
% furnished to do so, subject to the following conditions:
%
% The above copyright notice and this permission notice shall be included in all
% copies or substantial portions of the Software.
%
% THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
% IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
% FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
% AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
% LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
% OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
% SOFTWARE.
%
% Version 1.0.0 on 8/25/2023

function FID = magritek2d2mat(filename)

    
    fid = fopen(filename,'r');% Magritek File: little endian. 
                              % MATLAB will use a system-defautl byte order, 
                              % that is little endian for Windows.
    if fid == -1
        error('Cannot open the file.');
        return
    end

    owner_pros = fread(fid,1,'int32');
    format_data = fread(fid,1,'int32');
    version_v1_1 = fread(fid,1,'int32');
    dataType_504 = fread(fid,1,'int32');
    xDim = fread(fid,1,'int32');
    yDim = fread(fid,1,'int32');
    zDim = fread(fid,1,'int32');
    qDim = fread(fid,1,'int32');

    xlen = xDim*yDim*zDim*qDim;% Need to change the type?
    data = fread(fid,2*xlen,'float32'); % r1, i1, r2, i2, ...

    data = double(data);

    FID = data(1:2:end) + data(2:2:end)*1i; % Complex number
    FID = reshape(FID,xDim,yDim);
