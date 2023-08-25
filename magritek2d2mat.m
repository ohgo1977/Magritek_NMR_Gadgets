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
