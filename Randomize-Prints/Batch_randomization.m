% Script name Batch_randomization.m

clear; clc;

%% Initial conditions/batches

% Bambu can only print two dog bones per print/plate
% Bambu can print three 3-point bending specimen/plate
num_perplate = 3;

batches_200 = {'red_200', 'green_200', 'blue_200', 'purple_200', 'black_200';
    'red_200', 'green_200', 'blue_200', 'purple_200', 'black_200';
    'red_200', 'green_200', 'blue_200', 'purple_200', 'black_200';
    'red_200', 'green_200', 'blue_200', 'purple_200', 'black_200'};

batches_215 = {'red_215', 'green_215', 'blue_215', 'purple_215', 'black_215';
    'red_215', 'green_215', 'blue_215', 'purple_215', 'black_215';
    'red_215', 'green_215', 'blue_215', 'purple_215', 'black_215';
    'red_215', 'green_215', 'blue_215', 'purple_215', 'black_215'};

batches_230 = {'red_230', 'green_230', 'blue_230', 'purple_230', 'black_230';
    'red_230', 'green_230', 'blue_230', 'purple_230', 'black_230';
    'red_230', 'green_230', 'blue_230', 'purple_230', 'black_230';
    'red_230', 'green_230', 'blue_230', 'purple_230', 'black_230'};

%% Randomizing Batches and Saving Results
new_batches_200 = random_batch_sort(batches_200, num_perplate);
new_batches_215 = random_batch_sort(batches_215, num_perplate);
new_batches_230 = random_batch_sort(batches_230, num_perplate);

% Combining Batches
total_batches = [new_batches_200, new_batches_215, new_batches_230];

% Creating .csv file and saving results there
NewBatches_ID = fopen('New_Batches.csv', 'w');

saveorder_csv(total_batches, NewBatches_ID);

%% Randomizing Print Order and Saving Results
printing_order = random_print_order(total_batches);

% Creating .csv file and saving printing order there 
csvID = fopen('Printing_Order.csv', 'w');

saveorder_csv(printing_order, csvID);


%% Randomizing Testing Order and Saving Results 

testing_order = random_test_order(printing_order, num_perplate);

% Creating .csv file to save randomized testing order
testingID = fopen('Testing_Order.csv', 'w');

saveorder_csv(testing_order, testingID);
