---
author: Hermes Agent
description: Use when compiling local AudioCraft sounds parameters, structuring music
  prompts, or configuring songsee audio visualizers.
license: MIT
metadata:
  hermes:
    category: media
    tags:
    - music
    - audio
    - generation
    - EnCodec
    - MusicGen
    - Suno
    - spectrogram
name: music-and-audio-generation
version: 1.0.0
---

# Music and Audio Generation

Class-level playbook for audio processing, local generative music, remote AI song prompt crafting, and mechanical audio visualization.

---

## 1. Local Audio Generation (AudioCraft)
For local, high-fidelity generative music or sound design tasks.

### MusicGen (Text-to-Music)
- **Basic music generation**:
  ```python
  from audiocraft.models import MusicGen
  model = MusicGen.get_pretrained('facebook/musicgen-melody')
  model.set_generation_params(duration=8)
  wav = model.generate(['upbeat electronic synth-pop track'])
  ```
- **Melody conditioning**: Supply a melody audio file to guide the generation structure.
- **Stereo and continuation**: Load specialized stereo models or extend existing WAV inputs.
- **AudioGen**: Generate sound effects (e.g., "dog barking", "mechanical gears turning").
- **EnCodec**: Local neural compressor. Compress WAV to discrete tokens or reconstruct.

---

## 2. Songwriting & AI Song Crafting (Suno / Heartmula)
For vocal songs, parody tracks, and semantic lyrics.

### Heartmula Open-Source Music Gen
- Local Python API/Web UI utilizing heartcodec and HeartMuLa nodes to generate songs from lyrics + tags.
- Create virtual environments (requires Python 3.10) and manage dependency patches.

### Suno AI Prompt Crafting
- **Lyric formats**: Structure verses, choruses, and instrumental solos with labeled guides:
  ```text
  [Verse 1]
  [Chorus]
  [Guitar Solo]
  ```
- **Style tags**: Use 2-4 primary descriptor tags (e.g., `synthwave, high tempo, female vocals`). Avoid paragraphs in style fields.

---

## 3. Audio Visualization & Analysis (Songsee)
For CLI-based spectrogram extraction and sound profile inspections.
- Run `songsee` CLI to export Mel spectrograms, qdrant-vector-search profiles, and MFCC features. Used to verify audio content shapes or debug artifacts.