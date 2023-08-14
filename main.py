sample_list = [1, 1, 8, 4, 4, 2, 4, 8]
sample_dict = {}

for i in sample_list:
    if i in sample_dict:
        sample_dict[i] += 1
    else:
        sample_dict[i] = 1

print(sample_dict)
