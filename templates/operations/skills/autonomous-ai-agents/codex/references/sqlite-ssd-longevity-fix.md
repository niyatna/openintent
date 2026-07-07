# Codex CLI SQLite Heavy Logging / SSD Longevity Workaround

## Issue Summary
Codex CLI (especially active configurations running background otel/websocket transport) can log a massive volume of `TRACE` and `DEBUG` level rows to local SQLite feedback log files:
- `~/.codex/logs_2.sqlite`
- `~/.codex/logs_2.sqlite-wal`
- `~/.codex/logs_2.sqlite-shm`

This can result in extreme write amplification (extrapolating to ~640 TBW/year on active machines), which rapidly consumes consumer SSD write endurance (often limited to ~600 TBW) within less than a year.

## Solution / Workaround Procedure

1. **Verify Disk Churn & Log Distribution:**
   ```bash
   sqlite3 ~/.codex/logs_2.sqlite "SELECT level, count(*) FROM logs GROUP BY level;"
   ```

2. **Deploy Non-Destructive SQL Guard Trigger:**
   Add a database trigger to ignore all incoming log writes at the table layout level without deleting session settings or active history:
   ```bash
   sqlite3 ~/.codex/logs_2.sqlite "CREATE TRIGGER IF NOT EXISTS block_log_inserts BEFORE INSERT ON logs BEGIN SELECT RAISE(IGNORE); END;"
   ```

3. **Checkpoint & Truncate Active WAL Space:**
   Flush the write-ahead log (`-wal`) and shared memory (`-shm`) caches back into the main database:
   ```bash
   sqlite3 ~/.codex/logs_2.sqlite "PRAGMA journal_mode=WAL; PRAGMA wal_checkpoint(TRUNCATE);"
   ```

4. **Vacuum the Database to Free Bloated Sector Blocks:**
   ```bash
   sqlite3 ~/.codex/logs_2.sqlite "VACUUM;"
   ```
   *Verified typical output size change: Compacts databases from bloated 120MB+ states down to ~16MB.*
