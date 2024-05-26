from cryptography.fernet import Fernet

def load_key(key_file): #this function obtains the key from the file
   
 with open(key_file, 'rb') as f:
        return f.read()

def decrypt_file(input_file, output_file, key): #it receives the encrypted_file and the file to store the decrypted data "output_file" and the key 
   
   fernet = Fernet(key) #creates an object using the key
   with open(input_file, 'rb') as f:
        ciphertext = f.read() #reads the encrypted data and stores it and ciphertext variable
    
   plaintext = fernet.decrypt(ciphertext) #decrypts the encrypted data , which makes it plaintext 
    
   with open(output_file, 'wb') as f:
        f.write(plaintext) #opens the output file and writes the plaintext into it

def main():
    # asks for the key file name
    key_file = input("Enter the key file name (with extension): ")
    #asks for the encrypted file name
    encrypted_file = input("Enter the encrypted file name (with extension): ")
    #asks for the output file name
    output_file = input("Enter the output file name (with extension): ")
    
    try:
        key = load_key(key_file)#the loaded key from the file is stored into "key" variable
    except FileNotFoundError:
        print(f"Key file '{key_file}' not found. Please check the file name and try again.")
        return
    
    try:
        # this function decrypts the file
        decrypt_file(encrypted_file, output_file, key)
        print(f"Decrypted content saved to {output_file}")
    except FileNotFoundError:
        print(f"Encrypted file '{encrypted_file}' not found. Please check the file name and try again.")

if __name__ == "__main__":
    main()


