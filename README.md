# Fisher AIB Conference 2025 - Progressive Web App

A comprehensive conference portal for the 2025 AI in Business Conference at Fisher College of Business, The Ohio State University.

## Features
- **Multi-page conference portal** with main landing, agenda, and presentation search
- **Progressive Web App (PWA)** - Install as an app on iOS and Android devices
- **Full conference schedule** with expandable presentation sessions
- **Advanced presentation search** by author, topic, title, room, and time
- **WCAG 2.1 AA compliant** accessibility features
- **Mobile-responsive design** with OSU branding
- **Offline functionality** through service worker caching

## 📱 Install as Mobile App

### Android (Chrome/Edge):
1. Open the website in Chrome or Edge browser
2. Look for the "Add to Home Screen" prompt, or
3. Tap browser menu → "Add to Home Screen" or "Install App"
4. Confirm installation

### iOS (Safari):
1. Open the website in Safari
2. Tap the Share button (square with arrow)
3. Scroll down and tap "Add to Home Screen"
4. Tap "Add" to confirm

The installed app will work offline and provide a native app-like experience with OSU branding.

## Files
- `conference-main.html` - Main landing page with navigation
- `conference-agenda.html` - Complete conference schedule with expandable sessions
- `conference-presentation-search.html` - Advanced search and filtering interface
- `agenda.json` - Conference schedule and presentation data
- `manifest.json` - PWA manifest for app installation
- `sw.js` - Service worker for offline functionality and caching

## Local Testing
1. Clone this repository
2. Run a local server: `python3 -m http.server 8000`
3. Open `http://localhost:8000/conference-main.html`

## Live Demo
Visit: [https://ProfessorCastillo.github.io/FisherAIB2025/conference-main.html](https://ProfessorCastillo.github.io/FisherAIB2025/conference-main.html)

## Accessibility
This website meets Ohio State University's Minimum Digital Accessibility Standards (MDAS) and is fully compliant with WCAG 2.1 AA guidelines.
