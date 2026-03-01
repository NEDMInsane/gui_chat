import os
import sys

import ollama

class ModelInterface:
    def __init__(self, *args, **kwargs):
        #Server Configuration
        self.HOST = '192.168.1.15' #Make localhost if self-hosting
        self.PORT = '11434'
        self.CLIENT = None #This gets updated later.

        #Model Configuration settings
        self.MODEL_NAME = 'mistral-nemo:12b'
        self.USERNAME = 'User'
        self.CONTEXT_BUFFER = 15675
        self.EXIT_STATEMENTS = ['exit', 'quit', '/quit', '/exit']

        #Application Settings
        self.INTERFACE_APP = 'ollama' #if you want to use vllm or something else?

        #Context Paths
        self.PROMPT_PATHS = []
        self.ADDITIONAL_CONTEXT = []
        self.CURRENT_CONTEXT = [] # This will be a holder for all the context.

        self.setup_config(**kwargs)

    def setup_config(self, **kwargs):
        for key, value in kwargs.items():
            if key == 'username':
                self.USERNAME = value
            if key == 'additional_context':
                self.ADDITIONAL_CONTEXT.append(value)

        if self.INTERFACE_APP == 'ollama':
            self.CLIENT = ollama.Client(host=f'http://{self.HOST}:{self.PORT}')
        else:
            print(f'ERROR! {self.INTERFACE_APP} not supported') #maybe make this a logging level
            sys.exit()
        self.populate_prompt_paths()
        self.update_context()

    def populate_prompt_paths(self):
        for file_name in os.listdir(os.getcwd()):
            if file_name.find('prompt') != -1:
                self.PROMPT_PATHS.append(file_name)

    def update_context(self, context=None):
        if context is None:
            if self.PROMPT_PATHS:
                for file_path in self.PROMPT_PATHS:
                    try:
                        with open(file=file_path, mode='r') as file:
                            content = file.read()
                            self.CURRENT_CONTEXT.append({'role': 'system', 'content': content})
                    except FileNotFoundError:
                        print(f'File not found at {file_path}')
                    except Exception as e:
                        print(f'Something went wrong. {e}')
            else:
                self.CURRENT_CONTEXT.append({'role': 'system',
                                             'content': 'Begin the conversation by asking the user what they would like to do, fulfil requests within your programming.'})
                self.CURRENT_CONTEXT.append({'role': 'user',
                                             'content': '[Start Conversation]'})
        else:
            self.CURRENT_CONTEXT.append({'role': 'system', 'content': context})


    def send_to_model(self, new_message=None):
        if new_message is not None:
            self.CURRENT_CONTEXT.append({'role': 'user', 'content': new_message})

        full_response = self.CLIENT.chat(
            model = self.MODEL_NAME,
            messages = self.CURRENT_CONTEXT,
            stream = False,
            options = {
                #Sampling Options
                'temperature': 0.7,     #Randomness 0.0 - 2.0, higher = more creative
                'top_p': 0.9,
                'top_k': 40,

                #Context/Generation
                'num_ctx': self.CONTEXT_BUFFER,
                'num_predict': 128,      #Max Tokens to generate
                'seed': -1,              #Reproducability

                #Repetition Control
                'repeat_penalty': 1.1,  #1.0 = disabled
                'repeat_last_n': 64,    #How many tokens previous to look for repeats

                #Other
                'stop': self.EXIT_STATEMENTS,
                'num_batch': 512,
                'num_keep': 0,
                'penalize_newline': False,
                'presence_penalty': 0.0,
                'frequency_penalty': 0.0,
            }
        )
        content = full_response['message']['content']
        self.CURRENT_CONTEXT.append({'role': 'assistant', 'content': content})
        return f'{self.MODEL_NAME}: {content}'
