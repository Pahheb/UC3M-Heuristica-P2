# -- EJECUCION
for txt_file in tests/*.txt ; do
    if [ -f "$txt_file" ]; then
        echo "Testing: $txt_file..."
        
        # Run ASTARRodaje.py with parameter 1
        python3 sum.py "$txt_file" 1
        
        # Run ASTARRodaje.py with parameter 2
        python3 sum.py "$txt_file" 2
        
        echo "------------------------"
    fi
done
# -- EJECUCION
