# German A1 Vocab Quiz

A progressive web app for practicing German A1 vocabulary. Listen to words, choose the correct English meaning, and test your knowledge of German articles (der/die/das).

## Features

- **634 questions** — 479 vocab + 155 artikel, covering A1 level
- **Listen & Choose** — hear the German word spoken aloud via browser TTS
- **Speed control** — toggle between slow and normal playback
- **Artikel mode** — choose the correct article (der/die/das) for nouns
- **Choose question count** — pick 10, 25, 50, all, or a custom number per session
- **Add words** — add your own vocab or artikel questions directly in the app
- **Persistent storage** — custom words are saved in localStorage
- **Category badges** — words are tagged by group (Verb, Noun, Numbers, etc.)
- **Works offline** — PWA with service worker caching
- **iPhone ready** — add to home screen for a native app experience

## Word Categories

Months, Numbers, Clothing & Colors, Common Adverbs, Verbs, Nouns, Adjectives, Prepositions, Pronouns, Conjunctions, Interjections, and more.

## Quick Start

```bash
# Serve locally
python3 -m http.server 8080
```

Open http://localhost:8080 in your browser.

## Install on iPhone

1. Open the hosted URL in **Safari**
2. Tap **Share** (box with arrow)
3. Tap **Add to Home Screen**
4. It launches full-screen like a native app

## Deploy

Host the entire folder on any static hosting:

- **GitHub Pages** — push to a repo, enable Pages
- **Netlify** — drag and drop the folder
- **Vercel** — connect the repo

## Project Structure

```
├── index.html          # Single-page app (HTML + CSS + JS)
├── manifest.json       # PWA manifest
├── sw.js               # Service worker for offline support
├── icon-192.png        # App icon 192×192
├── icon-512.png        # App icon 512×512
├── .gitignore
├── LICENSE
└── README.md
```

## Data Source

Vocabulary compiled from Goethe-Zertifikat A1 word list.
