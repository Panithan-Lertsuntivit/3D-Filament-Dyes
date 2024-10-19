% Batch_randomization.m

clear; clc;

%% Initial batch

batches_200 = {'red_200', 'green_200', 'blue_200', 'purple_200', 'black_200';
    'red_200', 'green_200', 'blue_200', 'purple_200', 'black_200';
    'red_200', 'green_200', 'blue_200', 'purple_200', 'black_200';
    'red_200', 'green_200', 'blue_200', 'purple_200', 'black_200'};

new_size = 2;

input_batch = batches_200;

%% Creating Function/Algorithm to create a new randomized batch

% Data extraction
num_elements = numel(input_batch);
size = abs(new_size);

% Cell Array Dimensions and Creation
new_idx = randperm(num_elements);
columns = ceil(num_elements / new_size);
rows = new_size;

output_batches = cell([rows, columns]);

% Randomizing Elements into New Batch
for (i = 1:num_elements)
    output_batches(i) = input_batch(new_idx(i));
end


