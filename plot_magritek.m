%  ------------------------------------------------------------------------
%  File Name   : plot_magritek.m
%  Description : MATLAB function to read and plot Magritek 1D data (data.1d, spectrum.1d, and spectrum_processed.1d)
%  Developer   : Dr. Kosuke Ohgo
%  ULR         : https://github.com/ohgo1977/Magritek_NMR_Gadgets
%  Version     : 1.0.0
%
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

function vec = plot_magritek(filename,xlim_vec,plot_id,plot_switch)
        % Syntax:vec=plot_magritek(data_struct,xlim_vec,plot_id,plot_switch)
        % _unit)
        % filename: Magritek Binary data for spectrum. 'spectrum.1d' or 'spectrum_processed.1d'.
        % xlim_vec:the range of chemical shift for display
        % plot_id:optional, if your data has array, put the id of a spectrum which
        % you want to show.
        % Example:plot_magritek('spectrum_processed.1d',[0 100])
        % Example:vec = plot_magritek('spectrum_processed.1d',[-50 250],1,'on');
        
    if nargin < 4
        plot_switch = 'on';
    end

    if nargin < 3
        plot_id = 1;
    end

    [ppm,spc] = magritek1d2mat(filename);
    spc = real(spc);
    xaxis_vec = ppm;

    switch plot_switch
        case 'on'
            for ii = 1:length(plot_id)
                figure;
                plot(xaxis_vec,spc(:,plot_id(ii)));
                xlim(xlim_vec);
                set(gca,'xdir','reverse');
                set(gca,'box','off')% Delete top and right lines in the plot
                set(gca,'color','none')% Set the background to transparent
                set(gca,'ycolor','none')% Delte Yaxis 
                set(gca,'TickDir','out');% Tick outside
            end
    end
    vec = [xaxis_vec spc(:,plot_id)]';% Changing to a row vector.
