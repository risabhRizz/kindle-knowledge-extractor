from collections import defaultdict
from os.path import realpath
import os
import requests
import json
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.Model.list()

book_data = defaultdict(list)

def read_clippings_file(file_path):
    # specify delimiter
    delimiter = "=========="

    # open text file for reading
    with open(file_path, "r") as file:

        # read entire file contents
        contents = file.read()

        # split file contents into chunks based on delimiter
        chunks = contents.split(delimiter)

        # process each chunk
        for chunk in chunks:
            # here you can add your own analysis logic
            # for example, print each chunk
            chunk = chunk.strip()
            # print('-------------------------')
            # print(chunk)
            analyze_chunk(chunk)
            # print('xxxxxxxxxxxxxxxxxxxxxxxxx')

    pretty_print_analysis()

def analyze_chunk(chunk_str):
    lines = chunk_str.splitlines()
    if not lines:
        return
    
    try:
        book_title = lines[0]
        clipping_type = lines[1]
        
        # Check if clipping_type starts with '- Your Highlight'
        if clipping_type.startswith('- Your Highlight'):
            highlight_content = lines[3]
            book_data[book_title].append(highlight_content)
    except IndexError as e:
        pass
        # print(f'IndexError while processing the chunk: {} \n{chunk_str}')

    
def pretty_print_analysis():
    for book_title in book_data:
        print(f"Book: {book_title}, Highlights:\n")
        for highlight in book_data[book_title]:
            if len(highlight.split(' ')) > 1:
                print(f"{highlight}")
        print("====================================")
        
    print(f"Total books: {len(book_data)}, Total highlights: {sum([len(book_data[book_title]) for book_title in book_data])}")

    

# Request ChatGPT to anaylze the text
def chat_gpt_analysis(text_prompt):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json", 
        "Authorization": "Bearer " + os.getenv("OPENAI_API_KEY")
        }
    
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": f"{text_prompt}"}]
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    # Check the response status code
    if response.status_code == 200:
        # Convert the response to JSON format and print the result
        response_json = response.json()
        content = response_json['choices'][0]['message']['content']
        print(content)
    else:
        # The request failed
        print(f"The request failed. Response:{response.content}")


if __name__ == "__main__":
    # file_path = realpath("res/MyClippings.txt")
    # read_clippings_file(file_path)
    text_input = '''
    Book: The Time of Contempt (Andrzej Sapkowski), Highlights:

    Poor men can never afford anything, which is why they get called poor in the first place.’
    A sorceress bit viciously by serpents cold and vile, Observed the reptiles choke and die as she did herself smile!
    'Don't use titles with me,' Dijkstra winced.
    subdued the Power. He'd bound an element
    mineral, whose properties consisted of stifling
    her fingers burned. She shouted an incantation,
    out his orders!' The Trappers began to bustle.
    '''
    chat_gpt_analysis(f"Give me a summary of the book from these highlights: \n {text_input}")