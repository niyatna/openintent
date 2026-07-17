# Hermes Access Credential Registry

This directory contains non-secret access contracts for agent lane profiles.

Rules:

- Directory permissions: `700`.
- Registry file permissions: `600`.
- Do not store actual tokens, passwords, private keys, TOTP secrets, backup codes, cookies, or session dumps here unless a future encrypted credential-store design explicitly allows it.
- This registry references credential paths and environment variable names only.
- `.env`, auth files, cookies, token files, state databases, sessions, logs, caches, and disaster-recovery archives stay out of profile distribution repos.
- If a credential is missing or expired, use the recovery notes in `access-registry.yaml`; do not paste secrets into public chat.

Purpose:

- make account ownership explicit;
- prevent vague “tool exists therefore allowed” behavior;
- define autonomous, autonomous+log, and confirmation-required actions per domain;
- provide verification and recovery paths before claiming done.
