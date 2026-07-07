# CloakBrowser primary-route migration verification (2026-05-28)

Use this when moving dedicated Keiya/Galyarder owned-agent account workflows from Camofox-first to CloakBrowser persistent-profile-first.

## Scope

Update the whole routing layer, not only one browser skill:

- active profile/default browser posture text
- distribution mirror if the profile package has one
- class skills: `browser-routing`, `cloakbrowser-browser`, `agent-accounts`, `google-workspace`, `platform-operator-router`
- platform operator skills with stale browser-routing rules: `platform-operator-router`, `platform-operator-router`, `platform-operator-router`

## Migration wording

Preferred rule:

```text
CloakBrowser persistent profile first for dedicated Keiya/Galyarder owned-agent browser sessions.
Camofox/Camoufox is legacy/fallback only when CloakBrowser is blocked or a platform-specific skill still has a verified Camofox-based CRUD flow.
```

Avoid stale hard-gate phrases:

- `Camofox only`
- `mandatory Camofox`
- `No fallback`
- `route is **Camofox`
- `Camofox is the mandatory isolated browser`
- `CloakBrowser high-friction login experiment only`
- `Use only when Galih explicitly asks to test/use CloakBrowser`

## Verification ladder

Run the whole ladder before saying done:

1. `cloakbrowser-galyarder info` with OS-home environment; require `Installed: True` and OS-home cache/binary paths.
2. Confirm no profile-local home directory was recreated.
3. For each owner (`keiya`, `galyarder`), verify:
   - CloakBrowser Google profile dir exists and mode is `700`
   - Google cookie file exists and mode is `600`
   - cookie JSON parses and has nonzero cookies
   - `storage-state.cloakbrowser.json` exists and mode is `600`
4. Run fresh owner-state proof from CloakBrowser profile, not public Google marketing pages:
   - final host `myaccount.google.com`
   - title `Akun Google` / Google Account
   - expected email/account label visible
   - private sections visible (`Info pribadi`, `Keamanan`, `Data & privasi`, `Wallet`, `Langganan`)
   - no login form visible
5. Verify patched skills load with `skill_view` for all affected class/operator skills.
6. Grep active skill roots and browser-posture files for stale hard-gate patterns listed above.
7. Confirm no leftover Cloak/Chromium process tied to the Google CloakBrowser profile remains unless intentionally kept open.

## Reporting shape

When Galih asks if it is done, do not answer with process narrative first. Use one of:

```text
status: partial. patched: <files>. belum verified: <checks>.
```

or

```text
done. evidence: Cloak installed, Keiya+Galyarder owner-state active, cookies 600/nonzero, profile-home absent, stale-pattern grep clean, no leftover process.
```

If the task is interrupted mid-run, say `partial` explicitly and list the next exact move. Do not imply completion from a successful sub-step such as `manual-window-open`; that is only a browser-open proof, not owner-state proof.