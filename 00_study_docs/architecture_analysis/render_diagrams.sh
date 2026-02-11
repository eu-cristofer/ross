#!/bin/bash

# Navigate to the directory containing the script
cd "$(dirname "$0")"

# Function to render diagram
render_diagram() {
    local input_file="$1"
    local output_file="${input_file%.*}.png"
    
    echo "Rendering $input_file to $output_file..."
    
    if command -v mmdc &> /dev/null; then
        mmdc -i "$input_file" -o "$output_file"
    else
        echo "mmdc command not found. Attempting to use npx @mermaid-js/mermaid-cli..."
        # Using npx to execute mmdc from the package
        npx -p @mermaid-js/mermaid-cli mmdc -i "$input_file" -o "$output_file"
    fi
}

# Iterate through all .mermaid files in the current directory
for f in *.mermaid; do
    if [ -f "$f" ]; then
        render_diagram "$f"
    fi
done

