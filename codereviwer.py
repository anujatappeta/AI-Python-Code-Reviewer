from flask import Flask, render_template, request
import os
import subprocess

app = Flask(__name__)

# Ensure the upload folder exists
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # Limit file size to 16MB

def analyze_python_code(file_path):
    """Runs Pylint but ignores style warnings (like naming and redefinitions)."""
    try:
        result = subprocess.run(
            ["pylint", "--disable=C0103,W0621,C0114,C0115,C0116,C0303", file_path],
            capture_output=True, text=True
        )
        return result.stdout
    except Exception as e:
        return f"Error running Pylint: {e}"

# ✅ Missing Route is Added Here
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        if file and file.filename.endswith(".py"):
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(file_path)

            # Run Python code analysis
            review_result = analyze_python_code(file_path)

            return render_template("index.html", result=review_result)

    return render_template("index.html", result=None)

if __name__ == "__main__":
    app.run(debug=True)
