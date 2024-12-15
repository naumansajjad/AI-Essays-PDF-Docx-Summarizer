import openai
import PyPDF2
import docx
import os

#import openai credentials from os
openai.api_key=os.environ.get("OPENAI_API_KEY")

#file_path to the input file
"""Please note that pdf, docx files can now be used"""
file_path='user_input.txt'

#extract text from text file
def extract_text_from_text_file(file_path):
    with open(file_path, 'r') as file:
        text=file.read()
    return text

#extract text from pdf file
def extract_text_from_pdf_file(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text

#extract text from docx file
def extract_text_from_docx(file_path):
  doc = docx.Document(file_path)
  text = ''
  for paragraph in doc.paragraphs:
    text += paragraph.text
  return text

#Detect the file format of input file
def extract_text(file_path):
  if file_path.endswith('.pdf'):
    return extract_text_from_pdf(file_path)
  elif file_path.endswith('.docx'):
    return extract_text_from_docx(file_path)
  elif file_path.endswith('.txt'):
    return extract_text_from_txt(file_path)
  else:
    print('Unsupported file format')
    return ''


text = extract_text(file_path)

#print text given by user
"""print(text)"""

#Step 1 (make small chunks of text of 1000 words approx)
def text_chunker(text):
    words=text.split()
    processed_text=""
    for i in range(0, len(words), 1000):
        chunk=" ".join(words[i:i + 1000])
        response = process_text(chunk)
        processed_text += response.strip() + " "
    return processed_text.strip()

#Step 2 (Text Processing)
def process_text(text):
    #this step summarises chunks of text
    chat_completion=openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role":"user",
                "content":"Please summarize the following text in a precise and accurate manner: "
                + text +
                "The summary should be long than 15-20 lines and should capture the essence of the context and main ideas without losing important details."
            }
        ]
    )
    print("Analyzing input file.....")
    return chat_completion.choices[0].message.content.strip()

#calling functions of step 1 & 2
Chunked_Summary=text_chunker(text)

#Step 3 (file creating and storing summary)

def file_create_write(file_path, summary, summary_file_name):
    #extract filename without extension
    file_name=os.path.splitext(file_path)[0]
    #create folder with same name as file
    folder_name=file_name
    os.makedirs(folder_name, exist_ok=True)

    #create text file inside the folder
    file1_path=os.path.join(folder_name,summary_file_name)
    #write summary to the file
    with open(file1_path,'w') as file1:
        file1.write(summary)

file_create_write(file_path,Chunked_Summary,'Chunked_Summary.txt')

#Step 4 finally summarizing the chunked summary
Final_Summary=text_chunker(Chunked_Summary)

#file creation and storing summary
file_create_write(file_path,Final_Summary,'Conclusion_Summary.text')

#Step 5: Key_Notes Generation
def process_key_Notes(text):
    chat_completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages= [{
                'role':'user',
                'content':"Generate keynotes from the following text:"
                + text +
                "Make sure to accurately capture the meaning and represent it in numbered points in order."
                + "At the end, include a heading titled 'Bare Essentials' that summarizes the core concepts from the text."
            }])
    print("analyzing input file.....")
    return chat_completion.choices[0].content.strip()

def generate_keynotes(text):
    words=text.split()
    processed_text=""
    for i in range(0,len(words), 1000):
        chunk="".join(words[i:i+1000])
        response=process_key_Notes(chunk, )
        processed_text += response.strip()
    return processed_text.strip()

#generating keynotes chunk and processing
key_notes=generate_keynotes(Final_Summary)

file_create_write(file_path,key_notes,'Key_Notes.txt')

#All steps completed
print("The summary and Keynotes are generated and saved to the current directory.")