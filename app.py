import subprocess
import uuid
from pathlib import Path
from twelvelabs import TwelveLabs
import os
import uuid # Added for unique index name
import time # Added because time.sleep is used

def youtube_to_mp4(url, out_dir="/Users/yajatsharma/Downloads/factCheckerFR/videos", max_duration = 600):
    Path(out_dir).mkdir(exist_ok=True)
    output = f"{out_dir}/{uuid.uuid4()}.%(ext)s"

    subprocess.run([
        "yt-dlp",
        "-f", "bv*[height<=720]+ba/b",
        "--merge-output-format", "mp4",
        "--postprocessor-args", "ffmpeg: -movflags faststart",
        "--match-filter", f"duration < {max_duration}",
        "-o", output,
        url
    ], check=True)

    return output.replace("%(ext)s", "mp4")

def deleteMP4(file):
  Path(file).unlink()
  if not Path(file).exists:
    print('deleted')

os.environ["TL_API_KEY"] = "tlk_1H3EKJB1AMAH8A26XNV073KGZT34"
client = TwelveLabs(api_key = os.getenv("TL_API_KEY"))

# Generate a unique index name
unique_index_name = f"videos_{uuid.uuid4()}"
index = client.indexes.create(
    index_name = unique_index_name,
    models = [{"model_name": "pegasus1.2", "model_options": ["visual", "audio"]}]
)

if not index.id:
  raise RuntimeError("Failed to create an index")

print(f'Created index: {index.id}')

mp4_path = youtube_to_mp4("https://www.youtube.com/watch?v=FkWFkraLU8k")

# Corrected: use the variable mp4_path instead of the string literal "mp4_path"
asset = client.assets.create(
    method = "direct",
    file = open(mp4_path, "rb")
)
print(f"Created asset: {asset.id}")

indexed_asset = client.indexes.indexed_assets.create(
    index_id = index.id,
    asset_id = asset.id
)
print(f"Indexed asset: {indexed_asset.id}")

print("Waiting for indexing to complete.")
while True:
    indexed_asset = client.indexes.indexed_assets.retrieve(
        index_id=index.id,
        indexed_asset_id=indexed_asset.id
    )
    print(f"  Status={indexed_asset.status}")
    if indexed_asset.status == "ready":
        print("Indexing complete!")
        break
    elif indexed_asset.status == "failed":
        raise RuntimeError("Indexing failed")
    time.sleep(5)

text = client.analyze(
    video_id=indexed_asset.id,
    prompt="check for misinformation. Give in format: Summary: bullet points below, Misinformation: bullet points below (if none, say none)",
    temperature=0.2,
    max_tokens=1024,
    # You can also use `response_format` to request structured JSON responses
)

print(f"{text.data}")
deleteMP4(mp4_path)