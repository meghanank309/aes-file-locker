
# Mini AES File Locker

## 1. Introduction
Mini AES File Locker is a simple Python desktop application that demonstrates file encryption and decryption using AES-256-GCM. It provides a graphical interface for selecting files, generating encryption keys, and saving encrypted or decrypted output.

## 2. Objectives
- To demonstrate file encryption and decryption.
- To use AES-256-GCM for confidentiality and data integrity.
- To provide a simple graphical user interface.
- To demonstrate the importance of protecting encryption keys.

## 3. Technologies Used
- Python 3
- Tkinter
- Python Cryptography library
- AES-256-GCM

## 4. Features
- File selection using a Browse button.
- Random 256-bit encryption key generation.
- File encryption and output saving.
- File decryption using the original key.
- Detection of incorrect keys or modified encrypted data.

## 5. Methodology
The user selects a file and generates a random 256-bit key. During encryption, the application generates a fresh 12-byte nonce and encrypts the file using AES-GCM. The encrypted output contains a file-format header, nonce, ciphertext, and authentication tag.

During decryption, the application extracts the nonce and uses the supplied key to authenticate and decrypt the data. If authentication fails, the application rejects the operation.

## 6. Testing
The following functional tests were performed:

| Test | Expected Result | Status |
|---|---|---|
| File encryption | Encrypted file created | Pass |
| Correct-key decryption | Original data recovered | Pass |
| Incorrect-key decryption | Decryption rejected | Pass |

## 7. Limitations
- The application does not permanently store or recover lost keys.
- The user must keep the encryption key safe.
- Large files are currently read into memory in one operation.
- The application has not undergone a formal security audit.

## 8. Conclusion
Mini AES File Locker demonstrates the basic principles of file encryption and decryption using AES-256-GCM. Functional testing confirmed that files could be encrypted, recovered with the correct key, and rejected when an incorrect key was supplied.

## 9. Future Enhancements
- Password-based key derivation.
- Support for larger files through streaming encryption.
- Improved interface and key-management options.
