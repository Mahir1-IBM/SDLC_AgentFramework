# filename: setup_and_run_pong.sh
#!/bin/bash

# Install pygame if not already installed
pip show pygame &> /dev/null
if [ $? -ne 0 ]; then
    echo "Pygame not found. Installing pygame..."
    pip install pygame
else
    echo "Pygame is already installed."
fi

# Verify pygame installation
python - <<EOF
try:
    import pygame
    print("Pygame is installed correctly!")
    # Continue to run the pong game script
    exec(open("pong_game.py").read())
except ImportError as e:
    print("Pygame installation failed: ", e)
    exit(1)
EOF