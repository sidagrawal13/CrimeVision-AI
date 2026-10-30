import os
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

# 1. API Configuration
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("Missing GEMINI_API_KEY. Set it in your .env file.")
genai.configure(api_key=api_key)

# 2. System Instructions
SYSTEM_PROMPT = """
You are the Chief Forensic Intelligence System (CrimeVision AI).
Analyze the provided multimodal evidence (images, audio files, witness statements).
Always format your response using the following structured sections:
1. **Identified Evidence & Objects** (categorized by certainty)
2. **Chronological Reconstruction / Timeline**
3. **Risk & Priority Level** (Low / Medium / High / Critical with justification)
4. **Actionable Investigative Leads** (next steps for detectives/responders)
"""

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=SYSTEM_PROMPT
)

# 3. Forensic Analysis Function
def analyze_crime_scene(image_path: str = None, audio_file_path: str = None, witness_statement: str = None):
    print("🔍 [CrimeVision AI] Initializing Multimodal Forensic Ingestion...\n")
    contents = []
    
    if image_path and os.path.exists(image_path):
        img = Image.open(image_path)
        contents.append("Visual Evidence:")
        contents.append(img)
        
    if audio_file_path and os.path.exists(audio_file_path):
        print("🎙️ Uploading audio evidence for acoustic analysis...")
        audio_file = genai.upload_file(path=audio_file_path)
        contents.append("Acoustic / Call Evidence:")
        contents.append(audio_file)
        
    if witness_statement:
        contents.append(f"Witness / Dispatch Transcript Context:\n{witness_statement}")
        
    if not contents:
        raise ValueError("No evidence provided. Supply at least an image, audio file, or witness statement.")

    contents.append("\nGenerate the full forensic intelligence report based on the evidence above.")
    
    response = model.generate_content(contents)
    return response.text

if __name__ == "__main__":
    test_statement = (
        "Caller heard two loud bangs near the back alley at 02:15 AM, "
        "followed by screeching car tires heading north."
    )
    
    report = analyze_crime_scene(
        image_path=None,
        audio_file_path=None,
        witness_statement=test_statement
    )

    print(report)