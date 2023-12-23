
input_list = [1, 2, [3,[1,1,1], 4], 5, [6], 7, [8, [9, 10]]]

def extract_data(lst):
    func_list = []
    for item in lst:
        if type(item)==list:
            func_list.extend(extract_data(item))
        else:
            func_list.append(item)
    return func_list

output_list = extract_data(input_list)


print(output_list)