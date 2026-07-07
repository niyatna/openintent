# Reference: systematic-debugging

# Interactive Debugging Playbook

Interactive runtime debugging guides for Node.js and Python processes in terminal-safe contexts (PTY/REPL).

---

## 1. Node.js Debugging (node-inspect)
Debug Node.js applications by attaching to Chrome DevTools Protocol (CDP) interfaces.

### Workflow
- Start the process with inspection active:
  ```bash
  node --inspect-brk myscript.js
  ```
- Use the `node-inspect` debugger client to step through, inspect local context variables, set breakpoints, and resume execution.
- If remote port forward is needed, verify mapping via SSH before connecting.

---

## 2. Python Debugging (debugpy / pdb)
Debug Python code using either standard pdb or remote debugpy (DAP compatibility).

### Pdb (Standard Library REPL)
- Trigger inline breakpoints: `breakpoint()` (Python 3.7+) or `import pdb; pdb.set_trace()`.
- Run terminal session with `pty=true` so you can interact with the pdb prompt.
- **Commands**: `n` (next), `s` (step), `c` (continue), `p <variable>` (print), `q` (quit).

### Debugpy (Remote Debugging)
- Start script with debugpy listening:
  ```bash
  python3 -m debugpy --listen 5678 --wait-for-client myscript.py
  ```
- Connect a DAP client (e.g., debugger GUI or custom CDP router) to control execution.