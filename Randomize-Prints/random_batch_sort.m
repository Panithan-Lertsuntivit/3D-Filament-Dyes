function [output_batches] = random_batch_sort(initial_batch, batch_size)
% Function takes in initial batch or cell array (initial_batch), and the
% desired size for the new batches (batch_size).
% The initial batch will be randomly sorted into batches of (batch_size)

    % Data extraction
    num_elements = numel(initial_batch);
    
    % Cell Array Dimensions and Creation
    new_idx = randperm(num_elements);
    columns = ceil(num_elements / batch_size);
    rows = abs(batch_size);
    
    reordered_batches = cell([rows, columns]);
    
    % Randomizing Elements into New Batch
    for i = 1:num_elements
        reordered_batches(i) = initial_batch(new_idx(i));
    end

    % Grouping Batch Objects into 1 Cell
    num_batches = columns;
    output_batches = cell([num_batches, 1]);

    for j = 1:num_batches
        % Extracting objects from current batch
        objects = reordered_batches(:, j);
    
        % output array will be contain all of the objects
        num_objects = numel(objects);
        output = [];

        % Adding objects to output array one at a time
        for k = 1:num_objects
            output = [output, objects{k}, ' '];
        end
        % Getting rid of the last space 
        output(end) = [];

        % output array is saved as one cell in output_batches
        output_batches(j) = {output};
    end

end