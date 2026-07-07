# Agent-created Wallet Custody Audit

Use this reference when the assistant/Hermes previously generated or configured a crypto wallet for Galih and Galih asks whether the private key, seed phrase, or wallet file is safe.

## Trigger

- User says some version of: `you created the wallet`, `where is the private key`, `do you store it`, `is the seed safe`, `wallet aman kan`.
- A mining or payout workflow used a public wallet address, but wallet creation happened earlier in the same machine/tooling flow.

## Core distinction

Do not casually answer `I don't store it` if the agent helped create the wallet.

Say the precise custody model:

- The model/chat/memory must not store raw private keys, seed phrases, mnemonics, passphrases, cookies, or tokens.
- Mining jobs normally need only the **public wallet address**; this can appear in scripts/logs and is not a spend secret.
- The wallet secret may still exist in **local machine storage**: wallet database, key file, encrypted vault item, Bitwarden item, or local credential directory.
- If the agent created the wallet, answer from live evidence or say what is unverified.

## Safe audit workflow

Run only sanitized checks. Never print raw secrets.

1. **Recall provenance**
   - Search session history or notes for wallet creation/migration facts.
   - Identify whether a secure vault item exists (for example a `Pearl wallet` secure note) without printing fields.

2. **Inspect local wallet state by metadata only**
   - List wallet directories/files, paths, modes, and sizes.
   - Do not read or display secret file contents.
   - For Pearl/PRL examples, check likely runtime locations such as `.pearld`, project experiment directories, and secure credential/vault references.

3. **Scan for leaks without echoing values**
   - Search project/log/temp files for labels/patterns like `private key`, `seed phrase`, `mnemonic`, `passphrase`, `BEGIN PRIVATE KEY`, and secret assignments.
   - Output file path + line number + pattern label only, not the matching text.
   - Exclude dependency/vendor directories where possible.

4. **Separate public from secret markers**
   - `WALLET`, `prl1...`, pool worker names, and public addresses are not spend secrets.
   - Modal token placeholders like `YOUR_SECRET` are not proof of a real leaked token.
   - Strong findings are seed/mnemonic/private-key/passphrase values or local secret files with unsafe permissions.

5. **Report actual state**
   - Good wording: `aman dari chat/memory: yes; storage custody: probable/verified/unverified; here's the sanitized evidence`.
   - Bad wording: `I don't store it` with no caveat after the agent created the wallet.

6. **Remediate only with approval**
   - If leaked secret material is found, do not paste it.
   - Ask before deleting/moving files, rotating keys, or sweeping funds.
   - Prefer chmod/private-vault migration first, then rotation/sweep if exposure is real.

## Response shape

```text
koreksi:
- gua yang generate/config walletnya, jadi custody harus dibedain.

status:
- chat/memory: <no raw secret stored / unverified>
- mining scripts: <public address only / leak found>
- local storage/vault: <verified item/path metadata / unverified>

risk:
- <what could still expose funds>

next safe move:
- <audit vault existence / scan leaks / rotate if exposed>
```

## Pitfall from PRL session

In the PRL Modal mining flow, the assistant first said `I don't store private keys`, then Galih correctly challenged it because the assistant had generated/configured the PRL wallet earlier. The correct answer was not a blanket denial; it was a custody split:

- not stored in assistant chat/memory;
- miner uses only public `prl1...` address;
- local/vault storage must be verified separately;
- audit must be sanitized and never print raw wallet secrets.
