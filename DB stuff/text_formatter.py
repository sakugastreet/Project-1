# static_text_formatter.py
import re


def text_formatter(file_path):
    # this will be the final file with all the words in it
    all_words = []

    # Opens the file
    with open(file_path, "r") as file:

        file_contents = file.read().split()
        for word in file_contents:
            
            #cleans the word
            cleaned_word = clean_word(word)
            if cleaned_word != None:
                if cleaned_word not in all_words:
                    all_words.append(cleaned_word)


            
        all_words.sort()
        print(all_words)
            
def clean_word(word:str):
    if word[0].isalpha():
        return strip_punctuation(word).lower()



        
    strip_punctuation(word)

          
                


def strip_punctuation(word):
    # Define a regular expression pattern to match punctuation
    punctuation_pattern = r'[^\w\s]'
    
    # Use re.sub() to replace punctuation with an empty string
    return re.sub(punctuation_pattern, '', word)

def main():
    text_formatter("COMPLETE.txt")


if __name__ == "__main__":
    main()