# Threads Browser Posting Notes

Session: Keiya Threads first post setup/post attempt, 2026-05-17.

## What Worked

- Dedicated Threads credentials belong under:
  `/home/galyarder/.hermes/private/credentials/agents/<owner>/threads/`
- Account file can include:
  - `SERVICE=threads`
  - `PROFILE_URL=https://www.threads.com/@<username>`
  - `USERNAME=`
  - `PASSWORD=`
  - `TOTP_SECRET=`
  - `BACKUP_CODES_FILE=`
  - `COOKIES_FILE=`
- Use `account_totp.py` to generate the Meta/Threads TOTP code from the saved account file without printing the secret.
- Login via `https://www.threads.com/login` with username/password, then TOTP, can reach the logged-in composer.
- Text-only post can be composed and posted from browser tools and verified on the profile page.

## Important Pitfall

Hermes browser accessibility click on **Attach media** may not open or expose the OS file picker, so a text post can succeed while the image silently fails to attach.

Do not claim a Threads image post succeeded unless the post is verified on the profile/media tab with the image present.

## Safer Posting Sequence

1. Verify image file exists and is SFW/appropriate before posting.
2. Log in and verify the composer shows the intended account.
3. Enter caption.
4. Attach media.
5. Verify media preview appears in the composer before clicking Post.
6. Click Post.
7. Verify the live post URL on the profile and confirm whether media is present.

If media attachment cannot be verified, stop and report honestly. Options:
- use a headed/manual browser for file picker interaction,
- add a Playwright/CDP script capable of `setInputFiles` if an input[type=file] exists,
- or make a text-only post only if Galih approves that fallback.

## Public Action Boundary

Threads public posts/replies/follows/DMs/profile changes require explicit Galih approval. Once approved, the action still needs live verification before reporting success.
