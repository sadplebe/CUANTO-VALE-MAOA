from flask import Flask, render_template, request
import os
from datetime import datetime
import cv2

app = Flask(__name__)

def recognize_image(image_path):
    # Load the uploaded image and the cartoon image (template)
    uploaded_image = cv2.imread(image_path)
    cartoon_image = cv2.imread(os.path.join("static", "images", "cartoon_reference.png"))

    # Check if images are loaded properly
    if uploaded_image is None:
        return "Error: Uploaded image could not be loaded. Please check the file."

    if cartoon_image is None:
        return "Error: Image could not be loaded. Please check the file path."

    # Convert images to grayscale for easier feature detection
    gray_uploaded_image = cv2.cvtColor(uploaded_image, cv2.COLOR_BGR2GRAY)
    gray_cartoon_image = cv2.cvtColor(cartoon_image, cv2.COLOR_BGR2GRAY)

    # Create an ORB detector object
    orb = cv2.ORB_create()

    # Detect keypoints and descriptors in both images
    kp1, des1 = orb.detectAndCompute(gray_uploaded_image, None)
    kp2, des2 = orb.detectAndCompute(gray_cartoon_image, None)

    # Use a Brute-Force Matcher to compare descriptors
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)

    # Sort matches based on their distances (best matches first)
    matches = sorted(matches, key=lambda x: x.distance)

    # Calculate a "match score" based on the best matches
    match_score = len(matches)

    # Define a threshold for a match
    threshold = 10
    if match_score >= threshold:
        # Calculate inflation-adjusted value
        monthly_inflation_rate = 0.0039
        months_elapsed = (datetime.now().year - 1999) * 12 + datetime.now().month - 2
        cumulative_inflation_factor = (1 + monthly_inflation_rate) ** months_elapsed

        original_amount = 10000.00
        adjusted_value = original_amount * cumulative_inflation_factor

        current_year = datetime.now().year
        return f"MAOA vale ${adjusted_value:,.2f} MXN según la inflación anual desde 1999 a {current_year}."
    else:
        return "Intenta nuevamente."

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if "image" not in request.files:
            return render_template("index.html", result="Error: No file uploaded.")
        
        image_file = request.files["image"]
        if image_file.filename == "":
            return render_template("index.html", result="Error: No file selected.")
        
        # Save the uploaded image
        upload_path = os.path.join("static", "images", "uploaded_image.png")
        image_file.save(upload_path)
        
        # Recognize the image
        result = recognize_image(upload_path)
        return render_template("index.html", result=result)
    
    return render_template("index.html", result=None)

if __name__ == "__main__":
    app.run(debug=True)
