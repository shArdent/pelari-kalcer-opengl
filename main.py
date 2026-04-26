import sys
import os

# Add the 'src' directory to the Python path
sys.path.insert(0, os.path.abspath('src'))

# Import the main module from the src folder
import main

if __name__ == "__main__":
    main.main()