import os
import sys

import ollama

class ModelInterface:
    def __init__(self, *args, **kwargs):
        #Server Configuration
        self.host = '192.168.1.15' #Make localhost if self-hosting
        self.port = '11434'
        self.client = None #This gets updated later.

        #Model Configuration settings
        self.model_name = 'mistral-nemo:12b'
        self.username = 'User'
        self.context_buffer = 15675
        self.exit_statement = ['exit', 'quit', '/quit', '/exit']
        self.model_parameters = {
            #Sampling Options
            'temperature': 0.7,     #Randomness 0.0 - 2.0, higher = more creative
            'top_p': 0.9,
            'top_k': 40,

            #Context/Generation
            'num_ctx': self.context_buffer,
            'num_predict': 128,      #Max Tokens to generate
            'seed': -1,              #Reproducability

            #Repetition Control
            'repeat_penalty': 1.1,  #1.0 = disabled
            'repeat_last_n': 64,    #How many tokens previous to look for repeats

            #Other
            'stop': self.exit_statement,
            'num_batch': 512,
            'num_keep': 0,
            'penalize_newline': False,
            'presence_penalty': 0.0,
            'frequency_penalty': 0.0,
        }

        #Application Settings
        self.interface_app = 'ollama' #if you want to use vllm or something else?
        self.timeout = 1 #Set up for debugging, when away from network

        #Context Paths
        self.prompt_paths = []
        self.additional_context = []
        self.current_context = [] # This will be a holder for all the context.

        self.setup_config(**kwargs)

    def setup_config(self, **kwargs):
        for key, value in kwargs.items():
            if key == 'username':
                self.username = value
            if key == 'additional_context':
                self.additional_context.append(value)
            if key == 'server' or key == 'server_address' or key == 'host' or key == 'host_address':
                self.host = value
            if key == 'port':
                self.port = value
            if key == 'model' or key == 'model_name':
                self.model_name = value

        if self.interface_app == 'ollama':
            self.client = ollama.Client(host=f'http://{self.host}:{self.port}', timeout=self.timeout)
        else:
            print(f'ERROR! {self.interface_app} not supported') #maybe make this a logging level
            sys.exit()
        self.populate_prompt_paths()
        self.update_context()

    def populate_prompt_paths(self):
        for file_name in os.listdir(os.getcwd()):
            if file_name.find('prompt') != -1:
                self.prompt_paths.append(file_name)

    def update_context(self, context=None):
        if context is None:
            if self.prompt_paths:
                for file_path in self.prompt_paths:
                    try:
                        with open(file=file_path, mode='r') as file:
                            content = file.read()
                            self.current_context.append({'role': 'system', 'content': content})
                    except FileNotFoundError:
                        print(f'File not found at {file_path}')
                    except Exception as e:
                        print(f'Something went wrong. {e}')
            else:
                self.current_context.append({'role': 'system',
                                             'content': 'Begin the conversation by asking the user what they would like to do, fulfil requests within your programming.'})
                self.current_context.append({'role': 'user',
                                             'content': '[Start Conversation]'})
        else:
            self.current_context.append({'role': 'system', 'content': context})


    def send_to_model(self, new_message=None):
        if new_message is not None:
            self.current_context.append({'role': 'user', 'content': new_message})

        try:
            full_response = self.client.chat(
                model = self.model_name,
                messages = self.current_context,
                stream = False,
                options = self.model_parameters
            )
            content = full_response['message']['content']
            self.current_context.append({'role': 'assistant', 'content': content})
            return f'{self.model_name}: {content}'
        except Exception as e:
            return f'SYSTEM: Model Connection Error - {e}'

