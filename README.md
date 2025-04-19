![home](https://github.com/user-attachments/assets/2c73effe-47d7-49b0-a135-2188b12cc894)


# 🔍 Proxy Checker by Hades
multi-threaded Python script to automatically and quickly check **HTTP / SOCKS4 / SOCKS5** proxies.   You can choose from default GitHub sources, a custom URL, or manually input your own list!

---

## 🚀 Features

- ✅ Supports **HTTP**, **SOCKS4**, **SOCKS5**, or **all at once**
- 🌐 Proxy source options:
  - Default GitHub lists
  - Custom URL
  - Manual input (directly in the terminal)
- 🔄 Multi-threaded (up to 50 threads for maximum speed)
- 🎨 Color-coded results (green = alive, red = dead)
- 📄 Automatically saves working proxies to `live_proxies.txt`
- 🧾 Includes a custom signature branding by Hades 😎

---

## 🖥️ How to Run

### 1. Clone the repository

```bash
git clone https://github.com/username/proxy-checker-hades.git
cd proxy-checker-hades
```

### 2. Install the dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the program

```
python3 proxy_checker.py
```

### 📥 Output
A file called live_proxies.txt will be generated, containing working proxies in the format:
> http 123.456.78.90 8080
> 
> socks4 98.76.54.32 1080
>
> socks5 192.168.1.1 1080
