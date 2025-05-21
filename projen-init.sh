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
  echo "Initializing pyproject.toml with poetry..."
  poetry init -n
fi

# --- Set python version constraint to >=3.12,<4.0 ---
if grep -q '^\s*python\s*=' pyproject.toml; then
  echo "Updating existing Python version constraint..."
  sed -i.bak 's/^.*python *=.*/python = ">=3.12,<4.0"/' pyproject.toml
else
  echo "Inserting Python version constraint..."
  awk '
    /^\[tool.poetry.dependencies\]/ {
      print
      print "python = \">=3.12,<4.0\""
      next
    }
    { print }
  ' pyproject.toml > pyproject.tmp && mv pyproject.tmp pyproject.toml
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
  "dev_deps": [],
  "extras": {},
  "include": [],
  "exclude": [],
  "gitignore": [],
  "scripts": {},
  "source": [
    {
      "name": "pypi_",
      "url": "https://pypi.org/simple/",
      "priority": "default"
    }
  ],
  "main_branch": "main"
}
EOF

# --- Run projen synthesis ---
python .projenrc.py
