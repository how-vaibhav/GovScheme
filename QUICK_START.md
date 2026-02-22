# ⚡ QUICK START GUIDE

## 🎯 Just Want to Run Everything? (Windows)

### **1-Click Startup (Easiest)**
```
Double-click: START_SERVERS.bat
```

That's it! Both servers will start automatically.

---

## 📋 What Gets Created

| File | Purpose | Run Command |
|------|---------|-------------|
| `START_SERVERS.bat` | ⭐ Windows auto-startup | Double-click it |
| `run_all_servers.py` | Python startup script | `python run_all_servers.py` |
| `start_servers.sh` | Linux/Mac startup script | `./start_servers.sh` |
| `test_servers.py` | Test if servers work | `python test_servers.py` |

---

## 🚀 Running the Servers

### **Method 1: Windows Batch (Easiest)**
```bash
# Just double-click this file
START_SERVERS.bat
```

### **Method 2: PowerShell / CMD**
```bash
cd C:\Users\LENOVO\OneDrive\Desktop\GovScheme
python run_all_servers.py
```

### **Method 3: Django Management Command**
```bash
python manage.py runserver
python manage.py run_rasa_server &  # In separate terminal
```

---

## ✅ How to Know It's Working

You'll see this output:
```
============================================================
    GOVERNMENT SCHEMES PORTAL - STARTUP
============================================================

📦 Starting RASA Actions Server...
✅ RASA Actions Server started

🌐 Starting Django Development Server...
✅ Django Server started

============================================================
✨ Both servers are running!
============================================================

📍 Services available at:
   🌐 Main Portal: http://localhost:8000
   🤖 RASA API: http://localhost:5055
   🔧 Admin Panel: http://localhost:8000/admin
```

---

## 🧪 Test the Setup

After servers start, in **another terminal** run:
```bash
python test_servers.py
```

You'll see:
```
✅ Django Server: CONNECTED (HTTP 200)
✅ RASA Server: CONNECTED
✨ All servers are running and communicating!
```

---

## 📍 Access Points

Once running, visit:

- **Main Portal**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin  
- **RASA Actions**: http://localhost:5055/webhook
- **Database Admin**: http://localhost:8000/admin

---

## 🛑 Stop Everything

Press **Ctrl+C** in the terminal where you started the servers.

Both will shut down gracefully.

---

## ⚙️ How It Works (Behind the Scenes)

### Architecture
```
┌─────────────────────────────────────────────────┐
│                  Your Browser                   │
│              http://localhost:8000              │
└──────────────────┬──────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
        ▼                     ▼
┌──────────────────┐   ┌──────────────────┐
│  Django Server   │   │ RASA Bot Actions │
│  Port: 8000      │   │ Port: 5055       │
│                  │   │                  │
│ ✨ Handles:      │   │ ✨ Handles:      │
│ - Web Pages      │   │ - Bot Responses  │
│ - Authentication │   │ - Scheme Info    │
│ - Schemes List   │   │ - Custom Logic   │
│ - User Data      │   │ - NLU Intent     │
│ - Notifications  │   │                  │
└──────────────────┘   └──────────────────┘
```

Both servers communicate automatically:
- Django sends requests to RASA via `http://localhost:5055/webhook`
- RASA processes actions and returns responses
- Seamless bot integration!

---

## 🔄 Startup Flow

```
run_all_servers.py starts
        │
        ├─→ Start RASA Actions Server (Port 5055)
        │    Wait 3 seconds...
        │
        ├─→ Start Django Server (Port 8000)
        │
        └─→ Monitor both processes
             Keep them alive
             Auto-restart if crash
             Stop on Ctrl+C
```

---

## 💡 Key Features

✅ **One-Command Startup** - Start both with single command  
✅ **Auto-Monitoring** - Detects crashes and handles shutdown  
✅ **Clean Shutdown** - Gracefully stops both servers  
✅ **Integrated Logging** - See both server outputs  
✅ **Error Handling** - Clear error messages if some fails  

---

## ❓ FAQ

**Q: Do I need two terminal windows?**  
A: No! The startup script handles everything in one window.

**Q: What if a server crashes?**  
A: The startup script will detect it and notify you.

**Q: Can I change the ports?**  
A: Yes, edit `run_all_servers.py` in the server startup commands.

**Q: Does it work on Mac/Linux?**  
A: Yes! Use `start_servers.sh` or `python run_all_servers.py`.

**Q: How do I stop the servers?**  
A: Press Ctrl+C in the terminal. Both servers stop gracefully.

---

## 📞 Troubleshooting

### Port Already in Use?
```bash
# Windows - Find what's using port 8000
netstat -ano | findstr :8000

# Mac/Linux - Find what's using port 8000
lsof -i :8000
```

### RASA Won't Start?
```bash
# Make sure RASA is installed
pip install rasa rasa-sdk

# Check RASA installation
rasa --version
```

### Django Won't Start?
```bash
# Make sure Django is installed
pip install django

# Check Django installation
django-admin --version

# Check dependencies
pip install -r requirements.txt
```

---

**You're all set!** 🎉

Now double-click `START_SERVERS.bat` and enjoy your integrated bot system.
