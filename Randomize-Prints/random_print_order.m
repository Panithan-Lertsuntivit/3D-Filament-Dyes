function [print_order] = random_print_order(total_batches)
% Function takes a number of batches (batches), and randomizes their order
% for an unbiased print order (print_order)

    % Determining the number of batches and creating a randomized order
    num_batches = numel(total_batches);
    print_idx = randperm(num_batches);

    % Inialization of cell array
    print_order = cell([num_batches, 1]);

    % Randomizing the print order
    for i = 1:num_batches
        print_order{i} = total_batches{print_idx(i)};
    end
end