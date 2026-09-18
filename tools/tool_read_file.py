
def tool_read_file(file_path):
    with open(file_path) as f:
        content = f.readlines()
    return str(content)