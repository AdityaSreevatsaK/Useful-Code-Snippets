# from cryptography.fernet import Fernet
#
# # Generate and save key
# key = Fernet.generate_key()
# with open('secret.key', 'wb') as key_file:
#     key_file.write(key)
#
# # Load key
# with open('secret.key', 'rb') as key_file:
#     key = key_file.read()
#
# # Encrypt
# f = Fernet(key)
# with open('file.txt', 'rb') as file:
#     encrypted = f.encrypt(file.read())
# with open('file.txt.encrypted', 'wb') as encrypted_file:
#     encrypted_file.write(encrypted)
#
# # Decrypt
# with open('file.txt.encrypted', 'rb') as encrypted_file:
#     decrypted = f.decrypt(encrypted_file.read())
# with open('file_decrypted.txt', 'wb') as decrypted_file:
#     decrypted_file.write(decrypted)
