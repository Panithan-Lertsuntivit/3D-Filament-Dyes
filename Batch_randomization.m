% Batch_randomization.m

clear; clc;

%% Initial batch

batches_200 = {'red_200', 'green_200', 'blue_200', 'purple_200', 'black_200',
    'red_200', 'green_200', 'blue_200', 'purple_200', 'black_200',
    'red_200', 'green_200', 'blue_200', 'purple_200', 'black_200',
    'red_200', 'green_200', 'blue_200', 'purple_200', 'black_200'};

new_size = 2;

%% Creating Function/Algorithm to create a new randomized batch

% Data extraction
num_elements = numel(batches_200);
size = abs(new_size);

% Cell Array Dimensions and Creation
new_idx = randperm(num_elements);
rows = ceil(new_idx / new_size);
columns = new_size;

output_batches = cell([rows, columns]);


