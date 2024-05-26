import pandas as pd                                                            #this is used to read tables espically from Excel files
import re                                                                      #a library used for matching patterns
from cryptography.fernet import Fernet                                         # "cryptography.fernet" is a library used for symmetric encryption and "Fernet" ensures that the encrypted data cannot be read unless you have the key    

patterns = {                                                                   # few possible sensetive attributes and the format of their corresponding values
    'Names': r'\b[A-Z][a-z]*\s[A-Z][a-z]*\b',
    'Credit Cards': r'\b(?:\d[ -]*?){13,16}\b', 
    'Passwords': r'(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*#?&]{8,}'
}

def extract_sensitive_info(dl):                                                #this function takes datalist as input , searches every column in the file , applying the pattrens listed above and the matches are added to sensitive_info
    sensitive_info = []
    for column in dl.columns:
        for pattern_name, pattern in patterns.items():
            matches = dl[column].astype(str).str.findall(pattern)
            for match_list in matches:                                         
                for match in match_list:
                    sensitive_info.append(f"{pattern_name}: {match}")
    return sensitive_info

def save_to_file(data, filename):                                              #this function writes the extracted sensitive information to a text file
    with open(filename, 'w') as f:
        for item in data:
            f.write(f"{item}\n")

def encrypt_file(input_file, output_file, key):
    fernet = Fernet(key) #the key is generated using "fernet"
    
    with open(input_file, 'rb') as f:
        plaintext = f.read() #open the file with the extracted sensitive information and assign the data there into "plaintext" variable
    
    ciphertext = fernet.encrypt(plaintext)#executing the encryption and putting the encrypted data in "ciphertext" variable
    
    with open(output_file, 'wb') as f:
        f.write(ciphertext) #creating an output file to store the encrypted data "ciphertext" in it

def main():
    
    # asks for the excel file name
    xlsx_file = input("Enter the Excel file name (with extension): ")
    try:
        dl = pd.read_excel(xlsx_file) #reads the excel file and puts the data intp the dl variable
    except FileNotFoundError: #in case something wrong went with the excel file
        print(f"File '{xlsx_file}' not found. Please check the file name and try again.")
        return
    
    #sends the dl variable to the function to extract sensitive information and store it inside sensitive_info variable 
    sensitive_info = extract_sensitive_info(dl)
    
    # execute the save_to_file function and send the sensitive data along with the file name that we want to save the sensitive data in  
    save_to_file(sensitive_info, 'SENSITIVE.txt')
    
    # auto generate a key using Fernet 
    key = Fernet.generate_key()
    with open('secret.key', 'wb') as f:
        f.write(key) #saving this key as a file named key
    
    #execute the encrypt_file function and send the file that contains the sensitive information "SENSITIVE.txt" and the file name that we want the encrypted data to be stored in "encrypted.txt"
    encrypt_file('SENSITIVE.txt', 'encrypted.txt', key) 
    print("Sensitive information extracted and encrypted successfully.")

if __name__ == "__main__":
    main()


