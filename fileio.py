import logging


def read_conversation_file(file_path):
    content = ''
    try:
        with open(file_path) as file:
            return content('conversation')
    except FileNotFoundError:
        logging.log(logging.ERROR, 'File not found')
        return None
    except Exception as e:
        logging.log(logging.ERROR, e)
        return None