# NIAS DE CADA ALUMNO
NIA_ALUMNO1=495775
NIA_ALUMNO2=495861


# --- PREPARACION
rm "../../p2-$NIA_ALUMNO1-$NIA_ALUMNO2.zip"
rm -rf "../../p2-$NIA_ALUMNO1-$NIA_ALUMNO2/"
mkdir temp
mkdir -p ../log
touch ../log/log.txt
LOG="../log/log.txt"

cd temp
# --- PREPARACION


# --- ESTRUCTURA DE ARCHIVOS
mkdir parte-1
mkdir parte-1/CSP-tests/
mkdir parte-2
mkdir parte-2/ASTAR-tests/
# --- ESTRUCTURA DE ARCHIVOS


# --- COPIAR ARCHIVOS
# Memoria y autores
cp ../../../memoria/main.pdf "./$NIA_ALUMNO1-$NIA_ALUMNO2.pdf" >& $LOG\
    || echo "ERROR al copiar la memoria"
cp ../../autores.txt ./autores.txt 2>> $LOG \
    || echo "ERROR al copiar los autores"
# Parte 1
cp ../../parte-1/CSP-tests/* ./parte-1/CSP-tests/ 2>> $LOG  \
    || echo "ERROR al copiar los tests de la parte 1"
cp ../../parte-1/ESPMaintenance.py ./parte-1/ESPMaintenance.py >& $LOG \
    || echo "ERROR al copiar ESPMaintenance.py"
cp ../../parte-1/CSP-calls.sh ./parte-1/CSP-calls.sh 2>> $LOG \
    || echo "ERROR al copiar CSP-calls.sh"
# Parte 2
cp ../../parte-2/ASTAR-tests/*.csv ./parte-2/ASTAR-tests/ 2>> $LOG \
    || echo "ERROR al copiar los tests de la parte 2"
# Formato de los tests: mapaXX.csv
if ls ./parte-2/ASTAR-tests | grep -qv "^mapa[0-9]\{2\}\.csv$"; then
    echo "ALERT: No todos los archivos ASTAR-tests siguen el formato:\n
    - Formato requerido: mapaXX.csv\n"
fi
cp ../../parte-2/ASTAR-tests/output/* ./parte-2/ASTAR-tests/ 2>> $LOG \
    || echo "ERROR al copiar el output de la parte 2"
# Formato del output: mapaXX_XX.output y mapaXX_XX.stat
if ls ./parte-2/ASTAR-tests | grep -qvE "^mapa[0-9]{2}_[12]\.(output|stat)$|^mapa[0-9]{1,2}\.csv$"; then
    echo "ALERT: No todos los archivos ASTAR-tests siguen el formato requerido:\n
    - TEST: Formato requerido: mapaXX.csv \n
    - OUTPUT: Formato requerido: mapaXX_<num_h>.(output|stat)\n"

fi
cp ../../parte-2/ASTARRodaje.py ./parte-2/ASTARRodaje.py 2>> $LOG \
    || echo "ERROR al copiar ASTARRodaje.py"
cp ../../parte-2/ASTAR-calls.sh ./parte-2/ASTAR-calls.sh 2>> $LOG \
    || echo "ERROR al copiar ASTAR-calls.sh"
# --- COPIAR ARCHIVOS


# --- COMPRESION
zip -r "../../../p2-$NIA_ALUMNO1-$NIA_ALUMNO2.zip" . 2>> $LOG 1>/dev/null \
    || echo "ERROR al comprimir los archivos"
# --- COMPRESION


# --- OUTPUT
if [ -f "../../../p2-$NIA_ALUMNO1-$NIA_ALUMNO2.zip" ] && [ ! -s "../log/log.txt" ];then
    echo "ZIP creado correctamente"
else
    echo -e "ERROR al crear el ZIP:\n
    - Para más información consulte el archivo log/log.txt"
fi
# --- OUTPUT

# --- LIMPIEZA
cd ..
rm -r temp
# --- LIMPIEZA


