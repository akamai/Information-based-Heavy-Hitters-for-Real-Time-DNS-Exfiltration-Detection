def write_list_to_file(file_path, my_list):
    with open(file_path, "w") as file:
        file.write("\n".join(map(str, my_list)))


def read_list_from_file(file_path):
    return [line.strip() for line in open(file_path, "r")]
