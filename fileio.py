import logging


def read_conversation_file(file_path):
    columns = ''
    content = []
    try:
        with open(file_path) as file:
            columns = file.readline() # Throw away the columns?
            for line in file:
                if line.startswith('user'):
                    content.append({'role': 'user', 'content': f'{line.removeprefix('user,').replace("\"", '').strip()}'})
                if line.startswith('assistant'):
                    content.append({'role': 'assistant', 'content': f'{line.removeprefix('assistant,').replace("\"", '').strip()}'})
            return content
    except FileNotFoundError:
        logging.log(logging.ERROR, 'File not found')
        return None
    except Exception as e:
        logging.log(logging.ERROR, e)
        return None