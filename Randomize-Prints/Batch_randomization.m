% Script name Batch_randomization.m

clear; clc;

%% Initial conditions/batches

% Bambu can only print two dog bones per print/plate
num_perplate = 2;

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

% Randomizing Batches
new_batches_200 = random_batch_sort(batches_200, num_perplate);
new_batches_215 = random_batch_sort(batches_215, num_perplate);
new_batches_230 = random_batch_sort(batches_230, num_perplate);

% Creating file to save results
fileID = fopen('Printing_Batches.txt', 'w');

% Saving 200C Batches to file
[row_200, column_200] = size(new_batches_200);

fprintf(fileID, 'Batch Printing at 200C \r\n');
fprintf(fileID, '%-10s %-15s %-15s \r\n', 'Batch #', 'Object 1', 'Object 2');

for i = 1:column_200
    fprintf(fileID, '%-10d %-15s %-15s \r\n', i, new_batches_200{1, i}, new_batches_200{2, i});
end

% Saving 215C Batches to file
[row_215, column_215] = size(new_batches_215);

fprintf(fileID, '\r\n \r\nBatch Printing at 215C \r\n');
fprintf(fileID, '%-10s %-15s %-15s \r\n', 'Batch #', 'Object 1', 'Object 2');

for i = 1:column_215
    fprintf(fileID, '%-10d %-15s %-15s \r\n', i, new_batches_215{1, i}, new_batches_215{2, i});
end

% Saving 230C Batches to file
[row_230, column_230] = size(new_batches_230);

fprintf(fileID, '\r\n \r\nBatch Printing at 230C \r\n');
fprintf(fileID, '%-10s %-15s %-15s \r\n', 'Batch #', 'Object 1', 'Object 2');

for i = 1:column_230
    fprintf(fileID, '%-10d %-15s %-15s \r\n', i, new_batches_230{1, i}, new_batches_230{2, i});
end

% Closing file
fclose(fileID);



