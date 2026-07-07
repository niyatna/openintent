import json, shutil, os
from pathlib import Path

def sync_skills(src_profile="galyarder", dst_profile="default", skills_to_sync=[]):
    """
    Sync skills across Hermes profiles safely with backups.
    Usage example inside execute_code or terminal python.
    """
    if dst_profile == "default":
        dst_root = Path(os.environ.get("HERMES_HOME", "/home/galyarder/.hermes")) / "skills"
    else:
        dst_root = Path(os.environ.get("HERMES_HOME", "/home/galyarder/.hermes")) / "profiles" / dst_profile / "skills"
        
    src_root = Path(os.environ.get("HERMES_HOME", "/home/galyarder/.hermes")) / "profiles" / src_profile / "skills"
    
    import datetime
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    backup_root = Path(f"/tmp/{dst_profile}_skill_sync_backup_{date_str}")
    backup_root.mkdir(parents=True, exist_ok=True)
    
    report = []
    for rel in skills_to_sync:
        src = src_root / rel
        dst = dst_root / rel
        
        if not (src / 'SKILL.md').exists():
            report.append({"skill": rel, "error": "Source SKILL.md missing"})
            continue
            
        backup = None
        if dst.exists():
            backup = backup_root / rel
            if backup.exists(): shutil.rmtree(backup)
            backup.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(dst, backup)
            
        dst.parent.mkdir(parents=True, exist_ok=True)
        if dst.exists(): shutil.rmtree(dst)
        shutil.copytree(src, dst)
        
        for p in dst.rglob('*'):
            if p.is_dir():
                os.chmod(p, 0o755)
                
        report.append({"skill": rel, "copied": True, "backup": str(backup) if backup else None})
        
    return {"backup_root": str(backup_root), "synced": report}

if __name__ == "__main__":
    # Example usage
    # print(json.dumps(sync_skills("galyarder", "default", ["browser/cloakbrowser-browser"]), indent=2))
    pass
