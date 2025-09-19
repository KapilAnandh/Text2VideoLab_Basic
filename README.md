# Text2VideoLab_Basic

A **learning project** that generates short videos from text prompts using **Hugging Face open-source models**.  
Built with **Diffusers, Flask, and Docker**

---

## Features
- Generate AI videos from text prompts
- Uses Hugging Face `diffusers` pipeline (`TextToVideoZeroPipeline`)
- REST API with Flask (runs on port `1122`)
- Containerized with Docker
- Educational, beginner-friendly project

---

##  Setup

**Clone repo**
```bash
git clone https://github.com/your-username/Kapil-Text2VideoLab.git
cd Text2VideoLab_Basic

2. Install dependencies
pip install -r requirements.txt

3. Run Flask app
python app.py


App will run on: http://0.0.0.0:1122

4.Run with Docker
docker build -t kapil-text2video .
docker run -p 1122:1122 kapil-text2video

5.API Usage
Generate Video

POST /generate

{
  "prompt": "A calm ocean sunrise with gentle waves, cinematic wide-angle, ultra-realistic, 4K",
  "fps": 8
}


Response: output.mp4 file

**Author**
Kapil Anandh P
AI Engineer
Experimenting with open-source video generation
