# 🛠️ Projen Submodule

A reusable submodule template for bootstrapping Python Poetry projects using [Projen](https://github.com/projen/projen)

---

## 🚀 Quick Start

1. **Create and initialize your project**
   ```sh
   mkdir my-project && cd my-project
   git init
   ```

2. **Add this repo as a Git submodule**
   ```sh
   git submodule add --name projen-submodule -b main ../projen-submodule projen-submodule
   ```

3. **Run the setup script**
   ```sh
   ./projen-submodule/projen-init.sh
   ```

4. **Create your project config**

   Create a `.projenrc.projdata.json` file in the root directory:
   ```json
   {
     "name": "pencil_pusher",
     "version": "1.0.0",
     "description": "Pushes pencils.",
     "deps": [
       "boto3@^1.18",
     ],
     "dev_deps": [
       "bandit@*"
     ]
   }
   ```

   🔍 *Note on advanced dependencies*:

   Complex dependencies must be JSON-escaped:
   ```json
   "torch@{ url = \"https://download.pytorch.org/\" }"
   ```

5. **Install Projen and run it**
   ```sh
   poetry install
   poetry run python3 .projenrc.py
   ```

---

## 📁 Folder Structure

```
my-project/
├── .github/
│   ├── ISSUE_TEMPLATE/new-issue-template.md
│   └── workflows/
│       ├── on-push.yml
│       ├── dependabot-build-transfer.yml
│       └── dependabot-auto-merge.yml
├── src/
│   └── main.py
├── tests/
│   └── test_example.py
├── .projenrc.py (symlink from submodule)
├── .projenrc.projdata.json (your config)
├── Makefile
├── pyproject.toml
├── poetry.lock
├── .gitignore
├── .flake8
├── mypy.ini
```

🔧 Files marked with `*` in the original repo are **managed by Projen** and regenerated automatically when `.projenrc.py` runs.

---

## ✨ Features

- 📦 Modular config with `.projenrc.py` and JSON input
- 🧰 Built-in dev tools: `black`, `flake8`, `mypy`, `bandit`
- ✅ GitHub Actions CI for testing and releases
- 🤖 Dependabot Pip automation
- 🛠️ Handy Make targets:
  - `make install`
  - `make test`
  - `make build`
  - `make publish`
  - `make fixstyle`
  - `make lint`
