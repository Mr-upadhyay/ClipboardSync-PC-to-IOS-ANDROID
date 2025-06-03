# 📋 ClipboardSync-PC-to-IOS-ANDROID

Seamless screenshot sharing from Windows to mobile devices

No cloud. No sign-up. Just simple image sharing from clipboard to phone.

---

## ✨ What You Need

- A **Windows PC**
- An **iPad or Android phone**
- Both devices must be on the **same Wi-Fi**
- **Python** installed on your PC

---

## 🐍 Step 1: Install Python (Skip if already installed)

1. Go to: [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Click **Download Python** (latest version).
3. **Important:** When installing, check the box that says:  
   ✅ **“Add Python to PATH”**
4. Click **Install Now**.
5. After installation, close and reopen any terminal or PowerShell window.

To check if Python is installed, press `Windows + R`, type:

```
cmd
```

Then run:

```
python --version
```

You should see something like: `Python 3.12.1`

If `python` or `pip` is not recognized, restart your computer and try again.

---

## 🚀 Step 2: Download and Open the Folder

- Download the **ClipboardSync-PC-to-IOS-ANDROID** folder to your PC and extract it if it's zipped.

---

## 📦 Step 3: Install Required Software (Dependencies)

1. Open the folder.
2. Hold **Shift + Right-click** inside the folder and choose **“Open PowerShell window here”** or **“Open Terminal”**.
3. Run this command:

   ```bash
   pip install flask flask-cors pywin32 Pillow
   ```

> This installs the tools needed to run ClipboardSync.  
> Do this only once on your computer.

---

## ▶️ Step 4: Start ClipboardSync

- **Double-click `start_server.bat`** inside the folder.

> A black window will open and stay open. That means it’s running!  
> Don’t close it while using ClipboardSync.

---

## 🌐 Step 5: Open It on Your iPad or Phone

1. On your PC, **find your computer’s hostname**:()

   - Press `Windows + R`, type `cmd`, and press Enter  
   - Type this and press Enter:

     ```
     hostname
     ```

   - Copy the name shown (e.g., `MyLaptop123`)

2. On your phone or tablet, open a browser and go to:

   ```
   http://<your-hostname>:3000
   ```

   Example:
   ```
   http://MyLaptop123:3000
   ```

> 💡 **Bookmark this page** or **Add to Home Screen** on your phone for easy access next time!

---

## 🖼️ Step 6: Copy and View Images

- Copy any image (Ctrl+C) on your Windows PC  
- It will appear automatically on your phone  
- **Long-press the image** to copy or save it on your phone/tablet

---

## 🎯 Make It Even Easier

### ✅ On Your Phone:
- Bookmark the URL or Add to Home Screen

### ✅ On Your PC:
- **Right-click `start_server.bat` → Send to → Desktop (Create Shortcut)**
- Use the shortcut to launch ClipboardSync anytime

---

## 🧯 Tips

- Ensure both devices are on the **same Wi-Fi**
- Don't close the black window while using
- If image doesn’t show, tap **“Refresh”** on your phone

---

## 🧡 Made By

Siddharth Upadhyay – Hope it makes your life a little easier 🙂
