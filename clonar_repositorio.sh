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
    REQ_FILE_0=$(find "$DIRECTORIO" -name "requirements.txt" 2>/dev/null | head -n 1)
    
    if [ -n "$REQ_FILE_0" ]; then
        echo "Archivo requirements.txt encontrado en: $REQ_FILE_0"
        echo "Instalando dependencias..."
        pip install -r "$REQ_FILE_0"
        pip install dill
        pip install noise

    else
        echo "No se encontró un archivo requirements.txt en el repositorio."
    fi

    REQ_FILE=$(find "$DIRECTORIO" -name "viz.py" 2>/dev/null | head -n 1)
    
    if [ -n "$REQ_FILE" ]; then

        sed -i 's|def show(self, field=\"displacement\", component=(0, 0), frame=0, quiverdisp=False, \*\*kwargs):|def show(self, field=\"displacement\", component=(0, 0), frame=0, quiverdisp=False, ruta_save=None, **kwargs):|g' "$REQ_FILE"
        sed -i 's|keyword = field.replace(" ", "").lower()|keyword = field.replace(" ", "").lower()\n        plt.figure(figsize=(10, 10))|g' "$REQ_FILE"
        sed -i 's|plt.show()|if isinstance(ruta_save, str): plt.savefig(ruta_save, dpi=300)|g' "$REQ_FILE"
    fi
fi

    
    

