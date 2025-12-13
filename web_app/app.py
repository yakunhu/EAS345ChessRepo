from flask import Flask, render_template, request, redirect, url_for
from logic import analyze_fen
 
# Create the Flask app
app = Flask(__name__)

# Home Page
@app.route("/")
def index():
    return render_template("index.html")

# Result page - runs when the user submits the FEN form.
# Reads the FEN then sends it to analyze_fen()
# then sends the results to result.html.
@app.route("/analyze", methods=["POST"])
def analyze():
    fen = request.form.get("fen", "").strip()

    # If the box was empty then send them back to the form
    if fen == "":
        return redirect(url_for("index"))

    try:
        result = analyze_fen(fen)
    except Exception:
        #return to form
        return redirect(url_for("index"))
    
    # Send fen and result to result.html for display
    return render_template("result.html", fen=fen, result=result)

# Run the app
if __name__ == "__main__":
    app.run()
