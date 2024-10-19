function [output_batches] = random_batch_sort(initial_batch, new_size)
% Function takes in initial batch or cell array (initial_batch), and the
% desired size for the new batches (new_sizes).
% The initial batch will be randomly sorted into batches of (new_size)

% Data extraction
num_elements = numel(initial_batch);
size = abs(new_size);

new_idx = randperm(num_elements);

end