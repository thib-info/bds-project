
def get_index_html_content(path):
    with open(path, 'r') as file:
        content = file.read()
    return content


def get_app_layout():
    return get_index_html_content('./assets/index.html')
