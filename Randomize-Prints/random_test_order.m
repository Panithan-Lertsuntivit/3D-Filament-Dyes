function [testing_order] = random_test_order(total_batches, obj_per_batch)
% Function takes a number of batches (batches), and randomizes their order
% for an unbiased testing sequence [one at a time] (test_order)

    % Determining the number of objects and creating a randomized order
    num_batches = numel(total_batches);
    num_objects = num_batches * obj_per_batch;
    general_idx = randperm(num_objects);

    % Refining to get batch and order index
    batch_idx = ceil(general_idx / obj_per_batch);
    order_idx = rem(general_idx, obj_per_batch) + 1;

    % Inialization of cell array
    testing_order = cell([num_objects, 1]);

    % Saving testing order to a cell array
    for i = 1:num_objects
        object_idx = sprintf('Print_%d Object_%d', batch_idx(i), order_idx(i));    
        testing_order{i} = object_idx;
    end

end