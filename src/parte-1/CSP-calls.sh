#!/bin/bash

# Iterar del test-1 al test-6
for i in {1..6}
do
    echo "Ejecutando test-$i..."
    python3 CSPMaintenance.py CSP-tests/test-$i.txt
    if [ $? -ne 0 ]; then
        echo "El test-$i falló con código de salida $?. Abortando el script."
        exit 1
    fi
    echo "Test-$i completado."
done

echo "Todos los tests completados con éxito."
