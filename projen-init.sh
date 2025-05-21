#!/bin/sh

# Ensure we're not inside the submodule dir before linking
if [ "${PWD##*/}" = "projen-submodule" ]; then
  cd ..
fi

# Link to shared .projenrc.py and copy .projen folder
ln -sf ./projen-submodule/.projenrc.py .projenrc.py
cp -r ./projen-submodule/.projen .

# Show current directory for logging/debugging
pwd

# --- Ensure pyproject.toml exists ---
if [ ! -f "pyproject.toml" ]; then
  echo "Initializing pyproject.toml with Poetry-style metadata..."
  cat <<EOF > pyproject.toml
[project]
name = "$(basename "$PWD")"
version = "0.1.0"
description = ""
authors = [
  {name = "$(git config user.name)", email = "$(git config user.email)"}
]
readme = "README.md"
requires-python = ">=3.12,<4.0"
dependencies = []

[build-system]
requires = ["poetry-core>=2.0.0,<3.0.0"]
build-backend = "poetry.core.masonry.api"
EOF
else
  # --- Patch requires-python in existing pyproject.toml ---
  if grep -q '^\s*requires-python\s*=' pyproject.toml; then
    echo "Updating existing requires-python..."
    sed -i.bak 's/^\s*requires-python\s*=.*/requires-python = ">=3.12,<4.0"/' pyproject.toml
  else
    echo "Adding requires-python to [project] section..."
    awk '
      /^\[project\]/ {
        print
        found=1
        next
      }
      found && NF==0 {
        print "requires-python = \">=3.12,<4.0\""
        found=0
      }
      { print }
    ' pyproject.toml > pyproject.tmp && mv pyproject.tmp pyproject.toml
  fi
fi

# --- Add projen as a dev dependency ---
echo "Adding projen via poetry..."
poetry add --dev projen

# --- Create .projenrc.projdata.json ---
cat <<EOF >.projenrc.projdata.json
{
  "name": "$(echo ${PWD##*/} | sed 's/-/_/g')",
  "author": "$(git config user.name)",
  "email": "$(git config user.email)",
  "version": "0.0.1",
  "deps": [],
  "dev_deps": [projen@*],
  "extras": {},
  "include": [],
  "exclude": [],
  "gitignore": [],
  "scripts": {},
  "source": [
    {
      "name": "pypi_",
      "url": "https://pypi.org/simple/",
      "priority": "primary"
    }
  ],
  "main_branch": "main"
}
EOF

# --- Run projen synthesis ---
poetry run python .projenrc.py
