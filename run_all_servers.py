"""
Startup script to run both Django and RASA servers together
"""
import os
import subprocess
import sys
import time
import signal
from pathlib import Path

def run_servers():
    """Run Django and RASA servers concurrently"""
    
    django_path = r'c:\Users\LENOVO\OneDrive\Desktop\GovScheme'
    rasa_path = r'c:\Users\LENOVO\rasa_project'
    
    print("=" * 60)
    print("🚀 GOVERNMENT SCHEMES PORTAL - STARTUP")
    print("=" * 60)
    
    processes = []
    
    try:
        # Start RASA Actions Server (using lightweight Flask server)
        print("Starting RASA Actions Server...")
        print(f"   Location: {rasa_path}")
        print(f"   Port: 5005")
        
        # Use lightweight Flask-based server instead of full RASA framework
        # This works without RASA installation and Python version compatibility issues
        rasa_script = str(Path(rasa_path) / 'actions' / 'lightweight_server.py')
        rasa_cmd = [sys.executable, rasa_script]
        
        if sys.platform == 'win32':
            rasa_proc = subprocess.Popen(
                rasa_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
        else:
            rasa_proc = subprocess.Popen(
                rasa_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                start_new_session=True
            )
        
        processes.append(('RASA', rasa_proc))
        print("✅ RASA Actions Server started")
        
        # Wait a moment for RASA to initialize
        time.sleep(3)
        
        # Start Django Server
        print("\n🌐 Starting Django Development Server...")
        print(f"   Location: {django_path}")
        print(f"   Port: 8000")
        print(f"   URL: http://localhost:8000")
        
        os.chdir(django_path)
        django_cmd = [
            sys.executable, 'manage.py', 'runserver',
            '0.0.0.0:8000'
        ]
        
        django_proc = subprocess.Popen(
            django_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        processes.append(('Django', django_proc))
        print("✅ Django Server started")
        
        print("\n" + "=" * 60)
        print("Both servers are running!")
        print("=" * 60)
        print("\nServices available at:")
        print("   Main Portal: http://localhost:8000")
        print("   RASA API: http://localhost:5005")
        print("   Admin Panel: http://localhost:8000/admin")
        print("\nPress Ctrl+C to shutdown all servers\n")
        
        # Keep processes alive and monitor
        initial_wait = True
        while True:
            # Skip crash check for first 30 seconds to allow servers to fully start
            if initial_wait:
                print("\n⏳ Servers initializing... (will monitor after 30 seconds)\n")
                time.sleep(30)
                initial_wait = False
            
            # Simple status check (don't exit on first None)
            for name, proc in processes:
                if proc.poll() is not None:
                    try:
                        stdout, stderr = proc.communicate(timeout=1)
                        if stderr:
                            print(f"\n{name} output: {stderr}")
                    except:
                        pass
                    print(f"\n⚠️  {name} server process ended!")
                    time.sleep(1)
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down servers...")
        for name, proc in processes:
            try:
                proc.terminate()
                print(f"✅ {name} server stopped")
            except Exception as e:
                print(f"❌ Error stopping {name}: {e}")
        
        # Give processes time to terminate gracefully
        time.sleep(1)
        
        # Force kill if still running
        for name, proc in processes:
            if proc.poll() is None:
                try:
                    proc.kill()
                except:
                    pass
        
        print("\n✨ All servers stopped successfully")
        sys.exit(0)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        # Cleanup
        for name, proc in processes:
            try:
                proc.terminate()
            except:
                pass
        sys.exit(1)


if __name__ == '__main__':
    run_servers()
