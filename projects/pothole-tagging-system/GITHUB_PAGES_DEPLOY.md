# GitHub Pages Deployment Guide

Since GitHub Pages only serves static files, here's how to deploy the Pothole Tagging System to your portfolio:

## Option 1: Static Demo Page (Recommended)

Create a self-contained static version that uses mock data:

```bash
# Create static demo folder
mkdir -p /home/suchir/portfolio-website/projects/pothole-tagging-system/static-demo
cp /home/suchir/portfolio-website/projects/pothole-tagging-system/frontend/index.html \
   /home/suchir/portfolio-website/projects/pothole-tagging-system/static-demo/
```

Then edit `static-demo/index.html` to replace the API calls with mock responses (see below).

## Option 2: Deploy Full Backend Elsewhere + Static Frontend

1. **Deploy Backend** to Render/Railway/Heroku:
   - Push backend folder to GitHub repo
   - Connect to Render.com as Web Service
   - Build: `pip install -r requirements.txt`
   - Start: `python app.py`
   - Get URL: `https://your-app.onrender.com`

2. **Update Frontend** to use deployed backend:
   ```javascript
   // In frontend/index.html, change:
   const API_BASE = 'https://your-app.onrender.com/api';
   ```

3. **Deploy Frontend** to GitHub Pages:
   - Push frontend folder to your portfolio repo
   - Enable GitHub Pages in repo settings
   - Access at `https://ksuchirreddy.github.io/projects/pothole-tagging-system/`

## Option 3: Link to Local/External Demo (Current Setup)

Your portfolio already links to:
```
https://ksuchirreddy.github.io/projects/pothole-tagging-system/frontend/index.html
```

This works when the project folder is in your GitHub Pages repo.

---

## Making a Static Demo (Self-Contained)

Replace the `analyzeUploaded()` function in `frontend/index.html` with this mock version for GitHub Pages:

```javascript
async function analyzeUploaded() {
  if (!currentImageBase64) {
    alert('Please upload or select an image first.');
    return;
  }

  document.getElementById('loadingState').style.display = 'block';
  document.getElementById('resultsContainer').style.display = 'none';
  document.getElementById('analyzeBtn').disabled = true;

  // Simulate processing delay
  await new Promise(resolve => setTimeout(resolve, 1500));

  // Mock detection results for demo
  const mockDetections = [
    {
      bbox: [150, 200, 80, 60],
      area: 4800,
      circularity: 0.72,
      severity: 'Medium',
      confidence: 0.85
    },
    {
      bbox: [400, 300, 120, 100],
      area: 12000,
      circularity: 0.68,
      severity: 'High',
      confidence: 0.91
    }
  ];

  // Create a mock result image (just show original with overlay via canvas)
  const canvas = document.createElement('canvas');
  const ctx = canvas.getContext('2d');
  const img = new Image();
  img.onload = () => {
    canvas.width = img.width;
    canvas.height = img.height;
    ctx.drawImage(img, 0, 0);

    // Draw mock detections
    mockDetections.forEach((det, i) => {
      const [x, y, w, h] = det.bbox;
      const colors = { Low: '#10b981', Medium: '#f59e0b', High: '#fb923c', Critical: '#ef4444' };
      const color = colors[det.severity];

      ctx.strokeStyle = color;
      ctx.lineWidth = 3;
      ctx.strokeRect(x, y, w, h);

      ctx.fillStyle = color;
      ctx.fillRect(x, y - 25, 200, 25);
      ctx.fillStyle = '#000';
      ctx.font = '14px sans-serif';
      ctx.fillText(`Pothole #${i+1}: ${det.severity} (${(det.confidence*100).toFixed(0)}%)`, x + 5, y - 8);
    });

    document.getElementById('resultImg').src = canvas.toDataURL('image/jpeg');
    displayResults({ success: true, detections: mockDetections, total_count: mockDetections.length });
    document.getElementById('loadingState').style.display = 'none';
    document.getElementById('analyzeBtn').disabled = false;
  };
  img.src = currentImageBase64;
}
```

---

## Portfolio Integration (Already Done ✅)

The project is now linked in your `index.html` with:
- **Live Demo** button → `projects/pothole-tagging-system/frontend/index.html`
- Project card with tech tags
- Description highlighting OpenCV + Flask + Computer Vision

---

## File Structure for GitHub Pages

```
portfolio-website/
├── index.html                          # Main portfolio (links to project)
├── dashboard.html                      # Job tracker
├── projects/
│   └── pothole-tagging-system/
│       ├── frontend/
│       │   └── index.html              # ← Linked from portfolio
│       ├── backend/
│       │   ├── app.py
│       │   └── requirements.txt
│       ├── demo-data/
│       ├── static-demo/                # Optional: static version
│       ├── README.md
│       └── GITHUB_PAGES_DEPLOY.md
```

---

## Quick Test Locally

```bash
# Terminal 1: Start backend (requires Python packages)
cd /home/suchir/portfolio-website/projects/pothole-tagging-system/backend
python app.py

# Terminal 2: Start frontend
cd /home/suchir/portfolio-website/projects/pothole-tagging-system/frontend
python -m http.server 8080

# Open: http://localhost:8080
```

---

## Adding Demo Images

Place road images in `demo-data/`:
```bash
cp /path/to/road-photo.jpg /home/suchir/portfolio-website/projects/pothole-tagging-system/demo-data/
```

They'll auto-appear in the frontend for quick testing.