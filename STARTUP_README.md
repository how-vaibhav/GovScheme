# 🚀 Auto-Startup Configuration Guide

This guide explains how to automatically start both the Django and RASA servers together.

---

## 📋 What's New

We've created an integrated startup system that runs both servers simultaneously:

- **Django Server** (Port 8000) - Main web application
- **RASA Actions Server** (Port 5055) - Chatbot backend

---

## 🎯 Quick Start

### **Option 1: Windows (Easiest) ⭐**

Simply **double-click** the startup file:
```
START_SERVERS.bat
```

This will automatically:
1. Open a terminal window
2. Start RASA Actions Server (port 5055)
3. Start Django Server (port 8000)
4. Display all running services

---

### **Option 2: PowerShell / Command Prompt**

```powershell
cd C:\Users\LENOVO\OneDrive\Desktop\GovScheme
python run_all_servers.py
```

---

### **Option 3: Linux / Mac**

```bash
cd ~/OneDrive/Desktop/GovScheme
chmod +x start_servers.sh
./start_servers.sh
```

Or directly with Python:
```bash
python3 run_all_servers.py
```

---

### **Option 4: Manual (From separate terminals)**

**Terminal 1 - RASA Server:**
```bash
cd c:\Users\LENOVO\rasa_project
rasa run actions --port 5055
```

**Terminal 2 - Django Server:**
```bash
cd c:\Users\LENOVO\OneDrive\Desktop\GovScheme
python manage.py runserver
```

---

## 🔍 What to Expect

When you start the servers, you'll see:

```
============================================================
    GOVERNMENT SCHEMES PORTAL - STARTUP
============================================================

📦 Starting RASA Actions Server...
   Location: c:\Users\LENOVO\rasa_project
   Port: 5055
✅ RASA Actions Server started

🌐 Starting Django Development Server...
   Location: c:\Users\LENOVO\OneDrive\Desktop\GovScheme
   Port: 8000
   URL: http://localhost:8000
✅ Django Server started

============================================================
✨ Both servers are running!
============================================================

📍 Services available at:
   🌐 Main Portal: http://localhost:8000
   🤖 RASA API: http://localhost:5055
   🔧 Admin Panel: http://localhost:8000/admin

⏹️  Press Ctrl+C to shutdown all servers
```

---

## ✅ Access Points

| Service | URL | Purpose |
|---------|-----|---------|
| Main Portal | http://localhost:8000 | Upload your website here |
| Admin Panel | http://localhost:8000/admin | Manage schemes & users |
| RASA API | http://localhost:5055/webhook | Bot actions endpoint |
| Django Admin | http://localhost:8000/admin | Database management |

---

## 🛑 Stopping Servers

Simply press **Ctrl+C** in the terminal where you started the servers. Both will stop gracefully.

---

## 🐛 Troubleshooting

### **RASA Server fails to start**
- Make sure RASA is installed: `pip install rasa`
- Check that the RASA project path is correct in the script
- Verify port 5055 is not in use: `netstat -ano | findstr :5055` (Windows)

### **Django Server fails to start**
- Make sure you have all dependencies: `pip install -r requirements.txt`
- Check DEBUG is set to True in `.env`
- Verify port 8000 is not in use: `netstat -ano | findstr :8000` (Windows)

### **Both servers start but can't communicate**
- Verify `endpoints.yml` has action endpoint configured correctly:
  ```yaml
  action_endpoint:
    url: "http://localhost:5055/webhook"
  ```
- Check Django settings has RASA integration properly configured

---

## 📁 Files Created

```
GovScheme/
├── run_all_servers.py          # Main startup script
├── START_SERVERS.bat           # Windows shortcut
├── start_servers.sh            # Linux/Mac shortcut
├── STARTUP_README.md           # This file
└── schemesapp/management/commands/
    └── run_rasa_server.py      # Django management command
```

---

## 🔧 Advanced: Custom Configuration

To change server ports, edit `run_all_servers.py`:

```python
django_cmd = [
    sys.executable, 'manage.py', 'runserver',
    '0.0.0.0:8000'  # ← Change port here
]

rasa_cmd = [
    sys.executable, '-m', 'rasa', 'run', 'actions',
    '--port', '5055',  # ← Change port here
    '--debug'
]
```

---

## 📝 Environment Variables (Optional)

Set these environment variables to override defaults:

```bash
# Windows PowerShell
$env:RASA_PROJECT_PATH = "C:\path\to\rasa\project"
$env:DJANGO_PORT = "8000"

# Linux/Mac
export RASA_PROJECT_PATH=/path/to/rasa/project
export DJANGO_PORT=8000
```

---

## ✨ Benefits of This Setup

✅ **One-click startup** - Start both servers with a single command  
✅ **Auto-restart monitoring** - Detects if either server crashes  
✅ **Clean shutdown** - Gracefully stops both servers  
✅ **Easy management** - No need to open multiple terminal windows  
✅ **Development-friendly** - Watch for changes and auto-reload  

---

## 🚀 Next Steps

1. ✅ Run `START_SERVERS.bat` (on Windows) or `python run_all_servers.py`
2. ✅ Visit http://localhost:8000 in your browser
3. ✅ Test the chatbot on your portal
4. ✅ Check the RASA API at http://localhost:5055/webhook

---

## 📞 Support

If you encounter issues:

1. Check that Python 3.8+ is installed: `python --version`
2. Verify all dependencies are installed: `pip install -r requirements.txt`
3. Make sure RASA is installed: `pip install rasa`
4. Check that both ports (8000, 5055) are available
5. Run with `--debug` flag for more verbose output

---

**Happy coding!** 🎉

For more information, see the project README.md files.
