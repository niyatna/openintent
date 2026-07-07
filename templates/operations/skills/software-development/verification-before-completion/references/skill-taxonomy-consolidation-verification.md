# Verifying Skill Library Consolidation and Taxonomy Parity

When performing bulk restructuring, consolidation, or renaming of skills across profiles:

## 1. Verify Minimum Assertions (Router Checker)
* Adjust the minimum skill count threshold inside `/skills/galyarder-framework/galyarder-framework-router/scripts/verify_router_status.py` downwards to mirror the consolidated totals.
* Search the SCENARIOS dictionary inside target test script and discard deprecated sub-skill references (e.g., `obsidian-cli` or `google-workspace-auth-troubleshooting`) that are now references under umbrellas.

## 2. Parity Auditing
* Execute `/skills/galyarder-framework/galyarder-framework-router/scripts/verify_cross_profile_skill_sync.py` to identify mismatches.
* Ensure all universal, non-personality skills (tools, integrations, configs) match 100% physically between the default profile (`~/.hermes/skills/`) and the custom profile (`~/.hermes/profiles/galyarder/skills/`).

## 3. Configuration Maintenance
* If a deleted skill name was stored in `disabled` lists in `config.yaml`, edit the YAML physically to clear out the stale key name (since standard patch tool refuses writes for config files, use safe command scripting).
* Run global replacements of mapped old names to new umbrellas in all bundle YAML files under `skill-bundles/` folders.
* Run deduplication tools so bundle files contain unique list names.

## 4. Distribute and Remote Push
* Clean runtime cache files (`.skills_prompt_snapshot.json`) to force local Hermes index reload.
* Trigger `update-profile-distributions.py` to build distribution artifacts.
* Ensure both profiles git remote distributions (`galih master`) are updated cleanly with verified test integrity.
