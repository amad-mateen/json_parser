from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os
from pathlib import Path
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "change-me"  

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = BASE_DIR / "uploads"
UPLOAD_FOLDER.mkdir(exist_ok=True)
app.config["UPLOAD_FOLDER"] = str(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {"json"}

def allowed_file(filename: str) -> bool:
    """Check if the uploaded file has an allowed extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def search_json(data, key_term: str, path: str = ""):
    """Recursively search for (partial) key matches in JSON data.

    Args:
        data: The JSON-loaded Python object (dict/list/etc.).
        key_term: The search term (case-insensitive).
        path: Dotted path tracking the current traversal location.

    Returns:
        List of tuples of (matched_path, value).
    """
    results = []
    if isinstance(data, dict):
        for k, v in data.items():
            current_path = f"{path}.{k}" if path else k
            if key_term.lower() in k.lower():
                results.append((current_path, v))
            results.extend(search_json(v, key_term, current_path))
    elif isinstance(data, list):
        for idx, item in enumerate(data):
            current_path = f"{path}[{idx}]" if path else f"[{idx}]"
            results.extend(search_json(item, key_term, current_path))
    return results


@app.route("/", methods=["GET", "POST"])
def index():
    results = None
    key_term = ""
    filename = ""

    if request.method == "POST":
        # Validate that at least one source of JSON is provided
        file = request.files.get("json_file")
        existing_selected = request.form.get("existing_file", "").strip()
        key_term = request.form.get("key_term", "").strip()

        if (not file or file.filename == "") and not existing_selected:
            flash("Please choose a JSON file to upload or select an existing one.")
            return redirect(request.url)

        if not key_term:
            flash("Please enter a key to search.")
            return redirect(request.url)

        if file and file.filename != "":
            filename_raw = file.filename or ""
            if not allowed_file(filename_raw):
                flash("Invalid file type. Please upload a .json file only.")
                return redirect(request.url)

            filename = secure_filename(filename_raw)
            save_path = UPLOAD_FOLDER / filename
            file.save(save_path)
        else:
            filename = secure_filename(existing_selected)

        # Load the JSON data from the chosen file
        json_path = UPLOAD_FOLDER / filename
        if not json_path.exists():
            flash("Selected JSON file does not exist.")
            return redirect(request.url)

        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as exc:
            flash(f"Failed to parse JSON file: {exc}")
            return redirect(request.url)

        # Perform search
        results = search_json(data, key_term)

    # List existing JSON files in upload folder for UI display
    uploaded_files = [p.name for p in UPLOAD_FOLDER.iterdir() if p.is_file() and p.suffix.lower() == ".json"]

    return render_template(
        "index.html",
        results=results,
        key_term=key_term,
        filename=filename,
        uploaded_files=uploaded_files,
    )


# ------------------ Delete file route ------------------ #


@app.route("/delete/<path:filename>", methods=["POST"])
def delete_file(filename):
    """Delete a JSON file from the uploads directory."""
    safe_name = secure_filename(filename)
    file_path = UPLOAD_FOLDER / safe_name
    if file_path.exists():
        try:
            file_path.unlink()
            flash(f"Deleted {safe_name}.")
        except Exception as exc:
            flash(f"Failed to delete {safe_name}: {exc}")
    else:
        flash("File not found.")
    return redirect(url_for("index"))


if __name__ == "__main__":

    app.run(debug=True, port=5002) 