
import zipfile
import os

try:
    print("Attempting to extract the ZIP file...")
    with zipfile.ZipFile('CoarseWrithingBucket.zip', 'r') as zip_ref:
        # Create directory if it doesn't exist
        os.makedirs('extracted', exist_ok=True)
        # Extract all contents
        zip_ref.extractall('extracted')
    print("Extraction completed successfully!")
    
    # List extracted files
    print("\nExtracted files:")
    for root, dirs, files in os.walk('extracted'):
        for file in files:
            print(os.path.join(root, file))
            
except Exception as e:
    print(f"Error extracting ZIP file: {e}")
