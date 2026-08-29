# AI Pothole Tagging System

A computer vision-based pothole detection and tagging system using Python, Flask, and OpenCV. This project demonstrates end-to-end ML pipeline: from image processing → detection → severity classification → REST API → interactive web frontend.

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip (Python package manager)

### Installation & Run

```bash
# Navigate to backend directory
cd /home/suchir/portfolio-website/projects/pothole-tagging-system/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start backend server
python app.py
```

Backend will run on **http://localhost:5000**

### Frontend

Open `/home/suchir/portfolio-website/projects/pothole-tagging-system/frontend/index.html` in a browser, or serve it:

```bash
cd /home/suchir/portfolio-website/projects/pothole-tagging-system/frontend
python3 -m http.server 8080
```

Then visit **http://localhost:8080**

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/detect` | POST | Detect potholes (multipart file upload) |
| `/api/detect/base64` | POST | Detect potholes (base64 JSON) |
| `/api/history` | GET | Get detection history |
| `/api/stats` | GET | Get detection statistics |
| `/api/demo-images` | GET | List available demo images |
| `/api/demo/<filename>` | GET | Serve demo image |
| `/api/result/<filename>` | GET | Serve result image |

## 🧠 Detection Algorithm

The system uses classic computer vision (no deep learning required for demo):

1. **Preprocessing**: Grayscale → Gaussian Blur → CLAHE contrast enhancement
2. **Edge Detection**: Canny edge detection with morphological operations
3. **Contour Analysis**: Find contours, filter by area (500-50,000px²)
4. **Shape Properties**: Calculate circularity, polygon approximation
5. **Severity Classification**: Based on area and shape properties
6. **Confidence Scoring**: Combines circularity, vertex count, area

### Severity Levels
- **Low**: Small area (<1000px²)
- **Medium**: Medium area (1000-5000px²)
- **High**: Large area (5000-15000px²)
- **Critical**: Very large area (>15000px²)

## 📁 Project Structure

```
pothole-tagging-system/
├── backend/
│   ├── app.py              # Flask API server
│   ├── requirements.txt    # Python dependencies
│   ├── uploads/            # Uploaded images (auto-created)
│   └── results/            # Annotated result images (auto-created)
├── frontend/
│   └── index.html          # Interactive web UI
├── demo-data/              # Place demo road images here
└── README.md               # This file
```

## 🖼️ Adding Demo Images

Place road/pothole images in `demo-data/` folder (JPG, PNG, BMP). They'll appear in the frontend for quick testing.

Recommended demo images:
- Road with visible potholes
- Different lighting conditions
- Various road surfaces

## 🌐 Adding to GitHub Pages Portfolio

### Option 1: Static Demo (Recommended for GitHub Pages)

Since GitHub Pages only serves static files, create a static version:

```bash
# Create a static demo page
cd /home/suchir/portfolio-website/projects/pothole-tagging-system
mkdir -p static-demo

# Copy frontend to static-demo
cp frontend/index.html static-demo/
```

Then edit `static-demo/index.html` to use a mock API or pre-recorded results.

### Option 2: Link to Live Demo

Add a project card to your portfolio `index.html` linking to this live demo:

```html
<!-- In projects-grid section of index.html -->
<article class="card project-card">
  <div class="project-top">
    <div class="project-header">
      <span class="project-badge">Computer Vision</span>
      <a href="projects/pothole-tagging-system/frontend/index.html" 
         class="project-link" target="_blank" rel="noopener noreferrer">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
          <polyline points="15 3 21 3 21 9"></polyline>
          <line x1="10" y1="14" x2="21" y2="3"></line>
        </svg>
        <span>Live Demo</span>
      </a>
    </div>
    <h3 class="project-title">AI Pothole Tagging System</h3>
    <div class="project-date">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
        <line x1="16" y1="2" x2="16" y2="6"></line>
        <line x1="8" y1="2" x2="8" y2="6"></line>
        <line x1="3" y1="10" x2="21" y2="10"></line>
      </svg>
      <span>Aug 2026</span>
    </div>
    <p class="project-desc">
      Real-time computer vision system for automated pothole detection and severity tagging. 
      Built with OpenCV contour analysis, Flask REST API, and interactive web frontend.
    </p>
  </div>
  <div class="project-tags">
    <span class="tech-tag">Python</span>
    <span class="tech-tag">Flask</span>
    <span class="tech-tag">OpenCV</span>
    <span class="tech-tag">Computer Vision</span>
    <span class="tech-tag">HTML5/JS</span>
  </div>
</article>
```

### Option 3: Deploy Full Stack (Vercel/Render/Railway)

For full backend + frontend deployment:

1. **Backend** (Render/Railway):
   ```bash
   # Build command: pip install -r requirements.txt
   # Start command: python app.py
   ```

2. **Frontend** (Vercel/Netlify):
   - Update `API_BASE` in `frontend/index.html` to your deployed backend URL
   - Deploy frontend folder

3. **Update portfolio** with live demo link

## 🎯 Key Features Demonstrated

- **Computer Vision Pipeline**: OpenCV image processing from scratch
- **REST API Design**: Clean Flask endpoints with error handling
- **Real-time Frontend**: Drag-drop upload, live preview, detection overlay
- **Statistics Dashboard**: Session tracking, severity distribution
- **Demo Mode**: Pre-loaded test images for instant testing
- **Responsive UI**: Mobile-friendly, dark/light theme support

## 📝 License

MIT License - Feel free to use for learning/portfolio purposes.

---

**Built by K. Suchir Reddy** — [Portfolio](https://ksuchirreddy.github.io) · [GitHub](https://github.com/ksuchirreddy) · [LinkedIn](https://linkedin.com/in/ksuchirreddy)