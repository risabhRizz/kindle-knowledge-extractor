from collections import defaultdict
from os.path import realpath

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
        


if __name__ == "__main__":
    file_path = realpath("res/MyClippings.txt")
    read_clippings_file(file_path)