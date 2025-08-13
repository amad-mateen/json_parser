# JSON Key Search & File Manager

A simple Flask web application to search for keys in uploaded JSON files. Supports uploading, searching, listing, and deleting JSON files via a user-friendly web interface.

## Features
- Upload JSON files and store them on the server
- Search for keys (partial/case-insensitive match) in any uploaded JSON file
- View all matches with their dotted path and value
- Select from previously uploaded files
- Delete unwanted JSON files
- Flash messages for errors and actions

## How It Works
- Upload a `.json` file or select an existing one
- Enter a key term to search (partial/case-insensitive)
- The app recursively searches all keys in the JSON structure
- Results show the path and value for each match
- Uploaded files are stored in the `uploads/` folder

## Requirements
- Python 3.8+
- Flask

Install dependencies:
```bash
pip install flask
```

## Usage
1. Start the Flask app:
    ```bash
    python app.py
    ```
2. Open your browser at [http://localhost:5002](http://localhost:5002)
3. Upload a JSON file or select an existing one
4. Enter a key term and search
5. View results and manage files

## File Management
- Uploaded files are stored in the `uploads/` directory
- Use the delete button to remove files from the server

## Notes
- Only `.json` files are accepted
- Large or deeply nested files may take longer to search
- All actions are performed via the web interface

## License
MIT

## Author
amad-mateen
