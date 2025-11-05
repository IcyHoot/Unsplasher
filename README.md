<p align="center" width="1280" height="291">
  <img src="Unsplasher.png" alt="Image Downloader Logo" width="1280"/>
</p>


[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)
# Unsplasher

Unsplasher is a Auto-Image-Downloader made using Python, TKinter, Unsplash API & Beautiful Soup specially for AI training. You can download any image contained in Unplash, any resolution size [LATER] and how many you want.

# 🚀 Features

- Secure encryption of configuration data (password and API key) using AES-128 Fernet

- Unsplash API integration for automatic image search and download

- Encrypted local storage (```config.json```)

- Master password for authentication and decryption

- Simple and intuitive Tkinter interface

- Compatible with multiple operating systems (Windows, Linux, and macOS)


# 🧰 Usage
1. Run the script
``` python
python main.py
```
2. Create a master password (it will be used to generate the encryption key).

3. Enter your Unsplash API Key.

4. Provide the following information when prompted:

5. Search filter (e.g., “nature”, “city”, “space”)

6. Destination folder where images will be saved

7. Total number of images to download

_The program will automatically download the images, displaying progress and status messages along the way._

# Requirements
- Python 3.8+
- Tkinter
- Cryptography
- Requests
To Install:
```bash
  pip install requests cryptography tkinter
```

# 🧩 How its made?

The Image Downloader combines three main areas of Python development:

 1. Security and Encryption

- Uses the cryptography module with PBKDF2HMAC (SHA-256) to derive secure keys from the master password.

- Generates a persistent salt file so the same password always produces the same encryption key.

- Encrypts the config.json file using Fernet, which provides AES-128 encryption with HMAC authentication.



2. Graphical Interface

- Built with Tkinter and its native dialogs (simpledialog, messagebox, filedialog).

- Simple and direct interactions — the user defines a password, API key, search filter, destination folder, and number of images.

- Clear success, warning, and error messages guide the user through the process.

3. Unsplash API Integration

Uses the requests module to consume the Unsplash API endpoint:

``` html
https://api.unsplash.com/search/photos
```

- Performs paginated searches for images based on the user’s filter.

- Downloads and saves images to the chosen directory with unique filenames.

- Includes error handling for HTTP issues and rate limits.
