#!/usr/bin/env python3
"""
Test básico para verificar que la aplicación funciona correctamente
"""
import subprocess
import time
import requests
import sys
import os

def test_application():
    """Test básico de la aplicación"""
    print("🧪 Iniciando tests básicos de FitMotiv Backend...")
    
    # Cambiar al directorio del proyecto
    project_dir = "/Volumes/DiscoMacData/Previous Content/DevTools/proyectos/proyectos_python/fitmotiv-backend"
    os.chdir(project_dir)
    
    # Iniciar el servidor
    print("🚀 Iniciando servidor...")
    server = subprocess.Popen([
        "python3", "-m", "uvicorn", "app.main:app", 
        "--host", "0.0.0.0", "--port", "8000"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Esperar a que el servidor se inicie
    time.sleep(5)
    
    try:
        # Test 1: Health check
        print("🔍 Testing health endpoint...")
        response = requests.get("http://localhost:8000/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        print("✅ Health check passed")
        
        # Test 2: API info
        print("📋 Testing API info endpoint...")
        response = requests.get("http://localhost:8000/api")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "version" in data
        print("✅ API info passed")
        
        # Test 3: OpenAPI docs
        print("📚 Testing OpenAPI docs...")
        response = requests.get("http://localhost:8000/docs")
        assert response.status_code == 200
        print("✅ OpenAPI docs accessible")
        
        print("🎉 Todos los tests pasaron correctamente!")
        return True
        
    except Exception as e:
        print(f"❌ Error en los tests: {e}")
        return False
        
    finally:
        # Detener el servidor
        print("🛑 Deteniendo servidor...")
        server.terminate()
        server.wait()

if __name__ == "__main__":
    success = test_application()
    sys.exit(0 if success else 1)