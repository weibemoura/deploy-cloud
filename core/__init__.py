from tempfile import NamedTemporaryFile


def content_file(path):
    with open(path) as file:
        content = file.read()
    return content


def create_tempfile(content):
    tempfile = NamedTemporaryFile('w', encoding='utf-8', delete=False)
    tempfile.write(content)
    tempfile.flush()
    tempfile.close()
    return tempfile.name
