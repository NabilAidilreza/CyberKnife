# 🛠️ CyberKnife v1 — Python Multitool for CTFs

CyberKnife is a modular, Python-based multitool designed to assist in solving **Capture The Flag (CTF)** challenges efficiently. It consolidates essential utilities across various domains like cryptography, forensics, OSINT, and more—making it a must-have in your CTF toolkit.

---

## Features
### 1. 🔐 Cryptography
- Decode and encode using:
  - Base64, Base58, Base32, Base16, Base8
  - Caesar, Vigenère, ROT13
  - XOR (single/multi-byte)
  - AES (basic analysis if key/IV provided) => Not Done

### 2. 🧪 Forensics
- File inspection and extraction tools:
  - Metadata viewer
  - Hex viewer
  - PNG Dimensions Bruteforcer
  - GCode Checker

### 3. 🌐 OSINT => Not Done
- Gather intel using:
  - Wayback Machine
  - GEOINT Maps
  - Lookup Links
  - Social media footprinting via URL templates

### 4. 🔓 Crackers
- Brute-force and wordlist-based tools:
  - Bcrypt Cracker

### 5. 🌐 Web => Not Done
- Website analysis tools:
  - Domain Enumeration Tool
### 6. 🧩 Miscellaneous
- Handy utilities:
  - Netcat
  - Flag search across files
  - Bin-Dec-Hex to ASCII
---

## 🖥️ Usage

```bash
python cyberknife.py
```

Follow the prompt to select the working directory and navigate through modules.

---

## 📥 Installation

### Requirements

Make sure Python 3.7+ is installed. Then run:

```bash
pip install -r requirements.txt
```

---

## 🚧 Roadmap

- Clean up code
- Integrate API-based tools (Shodan, Hunter.io)
- Add RSA tools

---

## 🤝 Contribute

Pull requests are welcome! Have an idea or found a bug? Fork, patch, and submit.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

