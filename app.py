from flask import Flask, request, render_template_string, render_template, jsonify
import subprocess
from pathlib import Path
import uuid
import time
from twelvelabs import TwelveLabs
from openai import OpenAI
import os

app = Flask(__name__)

# Set your TwelveLabs API key
os.environ["TL_API_KEY"] = "API-KEY-HERE"
client = TwelveLabs(api_key=os.getenv("TL_API_KEY"))

client2 = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="API-KEY-HERE",
)

# Your youtube_to_mp4 function
def youtube_to_mp4(url, out_dir="videos", max_duration=600):
    Path(out_dir).mkdir(exist_ok=True)
    output = f"{out_dir}/{uuid.uuid4()}.%(ext)s"

    subprocess.run([
        "yt-dlp",
        "-f", "bv*[height<=720]+ba/b",
        "--merge-output-format", "mp4",
        "--postprocessor-args", "ffmpeg: -movflags faststart",
        "--match-filter", f"duration < {max_duration}",
        "-o", output,
        "--cookies", "cookies.txt",
        url
    ], check=True)

    return output.replace("%(ext)s", "mp4")

def deleteMP4(file):
    Path(file).unlink()
    if not Path(file).exists():
        print("Deleted:", file)

@app.route("/verifyAI")
def verifyAI():
    return render_template("verifyAI.html")

@app.route("/getStarted")
def get_started():
    return render_template("getStarted.html")

@app.route("/text")
def text_page():
    return render_template("text.html")

@app.route("/aboutUs")
def about_us():
    return render_template("aboutUs.html")

# HTML page with result display
HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Video Analysis - VerifyAI</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #fff;
            min-height: 100vh;
            overflow-x: hidden;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }

        /* Header */
        header {
            padding: 20px 0;
            position: relative;
            z-index: 10;
        }

        nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .logo {
            font-size: 28px;
            font-weight: bold;
            display: flex;
            align-items: center;
            gap: 10px;
            text-decoration: none;
            color: #fff;
        }

        .logo-icon {
            width: 40px;
            height: 40px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
        }

        .nav-links {
            display: flex;
            gap: 30px;
            list-style: none;
        }

        .nav-links a {
            color: #fff;
            text-decoration: none;
            font-weight: 600;
            transition: opacity 0.3s;
            font-size: 18px;
        }

        .nav-links a:hover {
            opacity: 0.8;
        }

        /* Page Title */
        .page-title {
            text-align: center;
            padding: 60px 0 40px 0;
        }

        .page-title h1 {
            font-size: 56px;
            margin-bottom: 15px;
            animation: fadeInUp 0.8s ease;
        }

        .page-title p {
            font-size: 20px;
            opacity: 0.9;
            animation: fadeInUp 1s ease;
        }

        /* Upload Section */
        .upload-content {
            padding: 40px 0 80px 0;
        }

        .upload-box {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            padding: 60px;
            border-radius: 30px;
            border: 2px dashed rgba(255, 255, 255, 0.3);
            text-align: center;
            transition: all 0.3s ease;
            max-width: 800px;
            margin: 0 auto;
        }

        .upload-box:hover {
            border-color: rgba(255, 255, 255, 0.6);
            background: rgba(255, 255, 255, 0.15);
        }

        .upload-icon {
            font-size: 80px;
            margin-bottom: 30px;
        }

        .upload-box h2 {
            font-size: 32px;
            margin-bottom: 20px;
        }

        .upload-box p {
            font-size: 18px;
            opacity: 0.9;
            margin-bottom: 40px;
        }

        .file-input-wrapper {
            position: relative;
            margin-bottom: 30px;
        }

        .file-input {
            display: none;
        }

        .file-label {
            display: inline-block;
            padding: 20px 50px;
            background: #fff;
            color: #667eea;
            border-radius: 50px;
            cursor: pointer;
            font-size: 18px;
            font-weight: bold;
            transition: all 0.3s ease;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            border: none;
        }

        .file-label2 {
            display: inline-block;
            padding: 10px 15px;
            background: #fff;
            color: #667eea;
            border-radius: 5px;
            cursor: pointer;
            font-size: 12px;
            font-weight: bold;
            transition: all 0.3s ease;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        }

        .file-label2:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.3);
        }

        .file-label:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.3);
        }

        .file-name {
            margin-top: 20px;
            font-size: 16px;
            opacity: 0.8;
        }

        .analyze-button {
            background: #fff;
            color: #667eea;
            padding: 18px 50px;
            border: none;
            border-radius: 50px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            margin-top: 20px;
        }

        .analyze-button:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.3);
        }

        /* Result Box */
        .result-box {
            margin-top: 40px;
            padding: 30px;
            background: rgba(76, 175, 80, 0.2);
            border: 2px solid rgba(76, 175, 80, 0.5);
            border-radius: 20px;
            text-align: left;
            max-height: 500px;
            overflow-y: auto;
        }

        .result-box h3 {
            font-size: 24px;
            margin-bottom: 20px;
            text-align: center;
            color: #a5f3a9;
        }

        .result-content {
            white-space: pre-wrap;
            line-height: 1.8;
            font-size: 16px;
        }

        .divider {
            display: flex;
            align-items: center;
            text-align: center;
            margin: 40px 0;
        }

        .divider::before,
        .divider::after {
            content: '';
            flex: 1;
            border-bottom: 1px solid rgba(255, 255, 255, 0.3);
        }

        .divider span {
            padding: 0 20px;
            opacity: 0.7;
        }

        .youtube-section {
            margin-top: 30px;
        }

        .youtube-input {
            width: 100%;
            padding: 18px 25px;
            font-size: 16px;
            border: none;
            border-radius: 50px;
            margin-bottom: 20px;
            background: rgba(255, 255, 255, 0.9);
            color: #333;
            outline: none;
            transition: all 0.3s ease;
        }

        .youtube-input:focus {
            background: #fff;
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.2);
        }

        .youtube-input::placeholder {
            color: #999;
        }

        /* Footer */
        footer {
            text-align: center;
            padding: 40px 0;
            background: rgba(0, 0, 0, 0.2);
            margin-top: 80px;
        }

        footer p {
            opacity: 0.9;
        }

        #hiddenText {
            display: none;
            margin-top: 20px;
            padding: 15px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 10px;
        }

        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @media (max-width: 768px) {
            .nav-links {
                display: none;
            }
            
            .page-title h1 {
                font-size: 42px;
            }
            
            .upload-box {
                padding: 40px 30px;
            }
        }
    </style>
</head>
<body>
    <header>
        <nav class="container">
            <a href="/verifyAI" class="logo">
                <div class="logo-icon">✓</div>
                VerifyAI
            </a>
            <ul class="nav-links">
                <li><a href="/verifyAI">Home</a></li>
                <li><a href="/getStarted">Features</a></li>
                <li><a href="/text">How It Works</a></li>
                <li><a href="/aboutUs">About</a></li>
            </ul>
        </nav>
    </header>

    <section class="page-title">
        <div class="container">
            <h1>Video Analysis</h1>
            <p>Upload videos to fact-check political content with AI</p>
        </div>
    </section>

    <section class="upload-content">
        <div class="container">
            <div class="upload-box">
                <div class="upload-icon">🎥</div>
                <h2>Upload Video File</h2>
                <p>Drag and drop your video file or click to browse (MP4 format)</p>
                
                <div class="file-input-wrapper">
                    <form method="POST" enctype="multipart/form-data">
                        <input type="file" name="videoFile" id="videoFile" class="file-input" accept=".mp4,video/mp4" onchange="handleVideoUpload()">
                        <label for="videoFile" class="file-label2">Choose Video File</label>
                        <div id="fileName" class="file-name"></div>
                        
                    <button type="submit" class="analyze-button" onclick="document.getElementById('loadingMessage').style.display='block'; var err = document.getElementById('errorBox'); if(err) err.style.display='none';">Analyze Video</button>
                    </form>
                </div>
                
                <div class="divider">
                    <span>OR</span>
                </div>

                <div class="youtube-section">
                    <form method=post>
                        <h3 style="margin-bottom: 20px;">Enter YouTube URL</h3>
                        <input type="text" name="url" id="youtubeUrl" class="youtube-input" placeholder="https://www.youtube.com/watch?v=...">
                        <button class="file-label" type="submit" onclick="document.getElementById('loadingMessage').style.display='block'; var err = document.getElementById('errorBox'); if(err) err.style.display='none';" style="padding: 15px 40px;">Analyze YouTube Video</button>                        <p id="loadingMessage" style="display: none; margin-top: 20px; padding: 20px; background: rgba(255, 193, 7, 0.3); border-radius: 15px; border: 2px solid rgba(255, 193, 7, 0.5);">
                        ⏳ Analyzing video... This may take several minutes. Please wait and do not refresh the page.
                        </p>
                    </form>
                </div>

                {% if result %}
                    {% if result.startswith('❌') %}
                    <div id="errorBox" style="margin-top: 30px; padding: 20px; background: rgba(244, 67, 54, 0.2); border: 2px solid rgba(244, 67, 54, 0.5); border-radius: 15px;">
                        <div class="result-content" style="text-align: center; font-size: 18px;">{{ result }}</div>
                    </div>
                    {% else %}
                    <div class="result-box">
                        <h3>✅ Analysis Complete!</h3>
                        <div class="result-content">{{ result }}</div>
                    </div>
                    {% endif %}
                {% endif %}
            </div>
        </div>
    </section>

    <footer>
        <div class="container">
            <p>&copy; 2026 VerifyAI. Fighting misinformation with artificial intelligence.</p>
            <p style="margin-top: 10px; opacity: 0.7;">Empowering citizens with truth and transparency.</p>
        </div>
    </footer>

    <script>
        let uploadedFile = null;

        function handleVideoUpload() {
            const fileInput = document.getElementById('videoFile');
            const fileName = document.getElementById('fileName');
            
            if (fileInput.files.length > 0) {
                uploadedFile = fileInput.files[0];
                
                if (!uploadedFile.type.includes('mp4')) {
                    alert('Please upload an MP4 video file');
                    uploadedFile = null;
                    return;
                }
                
                fileName.textContent = `Selected: ${uploadedFile.name} (${(uploadedFile.size / (1024 * 1024)).toFixed(2)} MB)`;
            }
        }
        function showLoadingMessage() {
        // Show the loading message when form is submitted
        document.getElementById('loadingMessage').style.display = 'block';
        return true; // Allow form to submit
        }
    </script>
</body>
</html>
"""

@app.route("/fact-check-text", methods=["POST"])
def fact_check_text():
    data = request.json
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "No text provided"}), 400

    response = client2.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a professional political fact checker. "
                    "Return your response STRICTLY in JSON with these fields:\n"
                    "{\n"
                    '  "verdict": "True | False | Misleading | Unverifiable",\n'
                    '  "confidence": number from 0 to 100,\n'
                    '  "explanation": "short explanation"\n'
                    "}"
                )
            },
            {
                "role": "user",
                "content": text
            }
        ],
        temperature=0.2
    )

    result = response.choices[0].message.content

    # IMPORTANT: parse JSON safely
    try:
        import json
        parsed = json.loads(result)
    except Exception:
        return jsonify({
            "verdict": "Unclear",
            "confidence": 0,
            "explanation": result
        })

    return jsonify(parsed)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    
    if request.method == "POST":
        url = request.form.get("url", "").strip()
        uploaded_file = request.files.get("videoFile")

        # Check if neither URL nor file is provided
        if not url and not uploaded_file:
            result = "❌ Error: Please provide a YouTube URL or upload a video file."
            return render_template_string(HTML_PAGE, result=result)
        
        # Check if URL is provided but invalid
        if url and not ('youtube.com' in url or 'youtu.be' in url):
            result = "❌ Error: Please enter a valid YouTube URL (must contain 'youtube.com' or 'youtu.be')"
            return render_template_string(HTML_PAGE, result=result)

        try:
            if url:
                print(f"Received URL: {url}")
                mp4_path = youtube_to_mp4(url)
                print("Downloaded video:", mp4_path)
            elif uploaded_file:
                out_dir = "videos"
                Path(out_dir).mkdir(exist_ok=True)
                filename = f"{uuid.uuid4()}.mp4"
                mp4_path = os.path.join(out_dir, filename)
                uploaded_file.save(mp4_path)
                print("Saved uploaded file:", mp4_path)

            # TwelveLabs processing
            unique_index_name = f"videos_{uuid.uuid4()}"
            index = client.indexes.create(
                index_name=unique_index_name,
                models=[{"model_name": "pegasus1.2", "model_options": ["visual", "audio"]}]
            )
            asset = client.assets.create(method="direct", file=open(mp4_path, "rb"))
            indexed_asset = client.indexes.indexed_assets.create(
                index_id=index.id,
                asset_id=asset.id
            )

            # Wait until ready
            while True:
                indexed_asset = client.indexes.indexed_assets.retrieve(
                    index_id=index.id,
                    indexed_asset_id=indexed_asset.id
                )
                print(f"Status: {indexed_asset.status}")
                if indexed_asset.status == "ready":
                    break
                elif indexed_asset.status == "failed":
                    raise RuntimeError("Indexing failed")
                time.sleep(5)

            # Analyze
            text = client.analyze(
                video_id=indexed_asset.id,
                prompt="check for misinformation. Give in format: Summary: bullet points below, Misinformation: bullet points below (if none, say none)",
                temperature=0.2,
                max_tokens=1024
            )
            print("Analysis result:\n", text.data)
            
            # Store result to display on page
            result = text.data

            # Delete local video after processing
            deleteMP4(mp4_path)

        except Exception as e:
            print("Error:", e)
            result = f"Error occurred: {e}"

    return render_template_string(HTML_PAGE, result=result)


if __name__ == "__main__":
    app.run(debug=True)