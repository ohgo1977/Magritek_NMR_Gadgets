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

    % if nargin < 5
    %     freq_unit = 'ppm';
    % end

    % if nargin < 6
    %     info_switch='off';
    % end

    [ppm,spc] = magritek1d2mat(filename);
    spc = real(spc);

    % switch freq_unit
    %     case 'ppm'
            xaxis_vec = ppm;
        % case 'Hz'
        %     freq_vec=[-sw/2:sw/(length(ppm)-1):sw/2];
        %     xaxis_vec=fliplr(freq_vec);
        % case 'kHz'
        %     freq_vec=[-sw/2:sw/(length(ppm)-1):sw/2];
        %     xaxis_vec=fliplr(freq_vec)/10^3;
    % end

    switch plot_switch
        case 'on'
            for ii = 1:length(plot_id)
    %             figure(plot_id(ii))%This line creats figures with figure numbers corresponding to plot_id.
    %             However, that style causes an issue when
    %             plot_data_struct is called in the other file to plot multiple
    %             dataset.
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

    % switch info_switch
    %     case 'on'
    %         title(data_struct.foldername,'interpreter','non');
    %         info_txt='';
    %         info_txt=[info_txt sprintf('LB:%s Hz\n',num2str(data_struct.LB))];
    %         info_txt=[info_txt sprintf('Zero Fill:%s pts\n',num2str(data_struct.ZeroFill))];
    %         info_txt=[info_txt sprintf('Original Size:%s pts\n',num2str(size(data_struct.FID,2)))];
    %         text(max(xlim),max(ylim),info_txt,'interpreter','non','VerticalAlignment','top')
    % end

    vec = [xaxis_vec spc(:,plot_id)]';% Changing to a row vector.
