function saveorder_csv(element_order, CSV_ID)
% Function takes an order of grouped elements (element_order) and a csv 
% file ID (CSV_ID) and saves the order of elements to the csv file. 
% The csv file will be closed within the function. 
    
    % Getting the number of grouped elements
    num_batches = numel(element_order);

    % Saving the grouped elements to the csv file
    for i = 1:num_batches
        % Saving the elements into the objects cell array, and determining
        % how many elements there are
        objects = strsplit(element_order{i});
        num_objects = numel(objects);

        fprintf(CSV_ID, '%d,', i);

        % Saving elements to the csv file one at a time
        for j = 1:num_objects
            fprintf(CSV_ID, '%s,', objects{j});
        end
        % Completed group of elements, preparing for next group
        fprintf(CSV_ID, '\n');
    end

    % Closing csv file before function ends
    fclose(CSV_ID);
end