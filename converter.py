from PyPDF2 import PdfReader
from os import getcwd
from datetime import datetime
import re

def pdf2text(path):
    reader = PdfReader(path)
    if len(reader.pages) == 1:
        return reader.pages[0].extract_text()
    else:
        return None

def orgTime(time):
    t_list = []
    c_list = []
    d_list = []
    for i in time.replace('\n', '').split(' '):
        tempVar = str()
        tempVar = i.replace('\n', '').replace(' ', '')
        
        if len(tempVar) > 1:
            if len(tempVar) > 3:
                t_list.append(tempVar)
            else:
                c_list.append(tempVar)
        tempVar = str()

    for t, c in zip(t_list, c_list):
        a,b = t.split('-')
        d_list.append(
            {
                "code":c,
                "time":{
                    'start':datetime.strptime(a, "%H:%M").strftime("%I:%M %p"),
                    'ends':datetime.strptime(b, "%H:%M").strftime("%I:%M %p")
                }
            }
        )

    return d_list

def removeTime(input_string, target_word):
    target_index = input_string.find(target_word)
    
    if target_index != -1:
        result = input_string[:target_index]
    else:
        result = input_string
    
    return result
def sbjwtime(text):
    pattern = r'\d+'
    output = list()
    
    for line in text:
        words = line.split()
        category = None
        numbers = []
        other_words = []

        for word in words:
            if word in ["Practical", "Theoretical"]:
                category = word
            elif word == "YUC" or re.search(r'\d+\s*[A-Za-z]+', word):
                break
            else:
                if re.match(r'\d+', word):
                    matches = re.findall(pattern, word)
                    numbers.extend(matches)
                else:
                    other_words.append(word)

        if category and numbers:
            category_with_code = " ".join([category] + other_words)
            numbers_str = " ".join(numbers)
            output.append(f"{category_with_code}: {numbers_str}")
    
    return output

def orgnizeText(text):
    sbjs = list()
    text = text.split('Sec Seq Activity Sun Tue Mon Thu Wed Building Room Staff')[1]    
    time = orgTime(text.split('Periods')[1])
    text = removeTime(text, 'Periods')
        
    for i in sbjwtime(text.split('\n')):
        sbjs.append(i)
    return sbjs, time

def main(path=f'{getcwd()}/file.pdf'):
    subjects, timeline = orgnizeText(pdf2text(path))
    subjects = sbjwtime(subjects)
    
    return subjects, timeline

if __name__ == '__main__':
    print(main())