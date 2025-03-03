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

    REQ_FILE=$(find "$DIRECTORIO" -name "viz.py" 2>/dev/null | head -n 1)
    
    if [ -n "$REQ_FILE" ]; then
        FRASE_ORIGINAL='def show(self, field="displacement", component=(0, 0), frame=0, quiverdisp=False, **kwargs):'
        FRASE_NUEVA='def show(self, field="displacement", component=(0, 0), frame=0, quiverdisp=False, ruta_save = None, **kwargs):'

        sed -i "s|$FRASE_ORIGINAL|$FRASE_NUEVA|g" $REQ_FILE

        FRASE_ORIGINAL='keyword = field.replace(" ", "").lower()'
        FRASE_NUEVA='keyword = field.replace(" ", "").lower()'$'\n''        plt.figure(figsize=(10, 10))'

        sed -i "s|$FRASE_ORIGINAL|$FRASE_NUEVA|g" $REQ_FILE
        
        FRASE_ORIGINAL='plt.show()'
        FRASE_NUEVA='if type(ruta_save) == str: plt.savefig(ruta_save, dpi=300)'

        sed -i "s|$FRASE_ORIGINAL|$FRASE_NUEVA|g" $REQ_FILE
fi

    
    

