# KundliKosh — Mobile (Expo / React Native)

The Android app. Built on Expo SDK 54 + Expo Router + react-native-svg. Bilingual (English + Hindi).

## Run locally

```bash
# 1) Install dependencies
npm install --legacy-peer-deps

# 2) Start the API in a separate terminal (from repo root)
cd ../api
PYTHONPATH=../engine uvicorn app:app --reload --host 0.0.0.0 --port 8000

# 3) Find your computer's LAN IP (e.g. 192.168.1.42) and point the app at it.
#    Edit app.json → expo.extra.apiBaseUrl to "http://<lan-ip>:8000"
#    OR set EXPO_PUBLIC_API_BASE in .env

# 4) Start Expo
npm run start

# 5) Open the QR code with Expo Go on your Android phone (free from Play Store)
```

## Folder structure

```
app/
  app/                  Expo Router file-based routes
    _layout.tsx         root layout (fonts, splash, profile hydration)
    index.tsx           gate → onboarding or tabs
    onboarding/         birth-data collection
    (tabs)/             home, kundli, match, devalok, ask
  src/
    api/                axios client + types matching FastAPI
    components/         PaperCard, NorthIndianKundli, PatronDeityCard, ...
    i18n/               EN + HI strings + locale store
    store/              AsyncStorage profile cache
    theme/              colors + typography tokens
```

## Visual identity

Mirrors the HTML preview at `../preview/preview.html`. Cosmic indigo background
+ parchment cards with double saffron borders. Deity illustrations are
hand-coded geometric SVGs — no AI raster art.

Custom logo slot is the dashed circle on the home screen — drop the file
into `assets/logo.png` and replace the placeholder in
`app/(tabs)/home.tsx` when ready.
