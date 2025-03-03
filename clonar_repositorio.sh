#!/bin/bash

# Configuración
DIRECTORIO="muDIC"
REPO_URL="https://github.com/PolymerGuy/muDIC.git"

# Verificar si la carpeta existe
if [ -d "$DIRECTORIO" ]; then
    echo "La carpeta '$DIRECTORIO' ya existe. No se requiere acción."
else
    echo "La carpeta '$DIRECTORIO' no existe. Clonando el repositorio..."
    git clone "$REPO_URL" "$DIRECTORIO"
    
    # Buscar requirements.txt dentro del repositorio clonado
    REQ_FILE=$(find "$DIRECTORIO" -name "requirements.txt" 2>/dev/null | head -n 1)
    
    if [ -n "$REQ_FILE" ]; then
        echo "Archivo requirements.txt encontrado en: $REQ_FILE"
        echo "Instalando dependencias..."
        pip install -r "$REQ_FILE"
    else
        echo "No se encontró un archivo requirements.txt en el repositorio."
    fi
fi

    
    

