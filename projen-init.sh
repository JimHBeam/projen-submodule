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

# Check if pyproject.toml exists, if not, initialize with poetry
if [ ! -f "pyproject.toml" ]; then
  echo "Initializing pyproject.toml with poetry..."
  poetry init -n
fi

# Add projen as a dependency
echo "Adding projen to the project with poetry..."
poetry add projen

# Generate .projenrc.projdata.json with generic project config
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

# Run projen synthesis
python .projenrc.py
