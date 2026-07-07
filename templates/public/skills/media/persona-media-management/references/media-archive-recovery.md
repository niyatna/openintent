# Media Archive Recovery Notes

Session lesson: PAP/selfie media may exist in several old locations, and some migration paths disappear after cleanup.

## Places to check

- `~/.hermes/image_cache/`
- `~/.hermes/migration/g-agent/*/assets/media/` when present
- `~/.local/share/Trash/files/g-agent-workspace/state/selfies/` for old generated persona selfies
- `~/.local/share/Trash/info/` can reveal deleted selfie filenames if the files directory still exists

## Safe recovery pattern

1. Find candidate files with `find`, not memory:
   ```bash
   find /home/galyarder -path '*/node_modules' -prune -o \
     -path '*/.cache' -prune -o \
     \( -iname 'selfie-*.jpeg' -o -iname 'AgACAg*.jpg' -o -iname 'CAACAg*.webp' \) -print
   ```
2. Verify the file exists and is readable.
3. Use `vision_analyze` before claiming what the image contains.
4. Send only a valid absolute path: `MEDIA:/absolute/path/to/file.jpeg`.
5. If the user says "bukan itu", stop guessing blindly. Create/send a contact sheet or ask them to identify by filename/number.

## Contact sheet fallback

If many selfie files exist, build a contact sheet so the user can choose:

```bash
mkdir -p /tmp/hermes_contact_sheets
cd /path/to/selfies
files=$(printf '%s\n' selfie-*.jpeg | tail -48)
montage $files -auto-orient -thumbnail 180x240 \
  -background white -fill black -pointsize 10 \
  -label '%f' -tile 6x -geometry 180x280+4+4 \
  /tmp/hermes_contact_sheets/keiya_selfies_recent48.jpg
```

If `montage` rejects an option, simplify the command rather than stopping.
