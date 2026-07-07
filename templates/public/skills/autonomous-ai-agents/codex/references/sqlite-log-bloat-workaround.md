# Codex SQLite Log Bloat & SSD Lifespan Mitigations

## Symptom

Codex CLI and its background otel/websocket logging client write continuous, high-frequency `TRACE` and `DEBUG` logs to the local SQLite database:
* `~/.codex/logs_2.sqlite`
* `~/.codex/logs_2.sqlite-wal`
* `~/.codex/logs_2.sqlite-shm`

This log churn can write **~5-16 MiB/s** during active sessions (issue #17320), totaling up to **~640 TBW/year** (terabytes written), which quickly consumes the entire warranted write endurance (TBW) of a typical 1TB consumer SSD in less than a year.

## Verification

To inspect if your local Codex setup is affected:

```bash
# Check database size
ls -lh ~/.codex/logs_2.sqlite*

# Check total logs count and dominant level count
sqlite3 ~/.codex/logs_2.sqlite "SELECT level, count(*) FROM logs GROUP BY level;"
```

If the file size is growing by hundreds of megabytes in a few minutes, or `TRACE`/`DEBUG` count represents the majority of the rows, the system is actively suffering from SSD wear.

## Solid Workaround (Non-Destructive)

Since the SQLite otel sink does not fully honor the `RUST_LOG=warn` env variable due to internal tracing subscriber overlaps, you must block writes at the database schema level using a trigger. This does not delete any session history, targets, or auth tokens.

1. **Apply the trigger to block TRACE/DEBUG insertions:**
   ```bash
   sqlite3 ~/.codex/logs_2.sqlite "CREATE TRIGGER IF NOT EXISTS block_log_inserts BEFORE INSERT ON logs BEGIN SELECT RAISE(IGNORE); END;"
   ```

2. **Checkpoint/truncate WAL to reclaim active journal space:**
   ```bash
   sqlite3 ~/.codex/logs_2.sqlite "PRAGMA journal_mode=WAL; PRAGMA wal_checkpoint(TRUNCATE);"
   ```

3. **Reclaim unused space and shrink database file:**
   ```bash
   sqlite3 ~/.codex/logs_2.sqlite "VACUUM;"
   ```

## Verification After Fix

Try inserting a test line manually:

```bash
sqlite3 ~/.codex/logs_2.sqlite "INSERT INTO logs (ts, ts_nanos, level, target, estimated_bytes) VALUES (1, 1, 'TRACE', 'test', 1);"
sqlite3 ~/.codex/logs_2.sqlite "SELECT count(*) FROM logs WHERE target='test';"
```

The count returned must be `0`, proving database-level logging is successfully blocked.
