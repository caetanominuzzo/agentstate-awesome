#!/usr/bin/env bash
set -euo pipefail

# Scaffold a new agentstate-awesome item interactively.
# Usage: ./scripts/new-item.sh

CATEGORIES=("integrations" "skills" "modes" "orchestration" "knowledge" "meta")

echo "=== New agentstate-awesome item ==="
echo

# Category
echo "Categories: ${CATEGORIES[*]}"
read -rp "Category: " CATEGORY
if [[ ! " ${CATEGORIES[*]} " =~ " ${CATEGORY} " ]]; then
  echo "Error: invalid category '$CATEGORY'" >&2; exit 1
fi

# Item name
read -rp "Item ID (kebab-case, e.g. stripe, systematic-debugging): " ITEM_ID
if [[ ! "$ITEM_ID" =~ ^[a-z0-9][a-z0-9-]*$ ]]; then
  echo "Error: ID must be kebab-case (lowercase, hyphens, no leading hyphen)" >&2; exit 1
fi

# Display name
read -rp "Display name (e.g. Stripe, Systematic Debugging): " DISPLAY_NAME

# Description
read -rp "Description (1-2 sentences): " DESCRIPTION

# Subcategory (optional)
read -rp "Subcategory (optional, press enter to skip): " SUBCATEGORY

# Script name
if [[ "$CATEGORY" == "integrations" ]]; then
  SCRIPT_NAME="${ITEM_ID//-/_}_cli.py"
  DEST_DIR="scripts/integrations/${ITEM_ID}"
elif [[ "$CATEGORY" == "skills" ]]; then
  SCRIPT_NAME="SKILL.md"
  DEST_DIR="skills/${SUBCATEGORY:+$SUBCATEGORY/}${ITEM_ID}"
else
  SCRIPT_NAME="${ITEM_ID//-/_}.py"
  DEST_DIR="scripts/${CATEGORY}/${ITEM_ID}"
fi

# Env vars
ENV_VARS=()
while true; do
  read -rp "Add an env var? (name or enter to skip): " ENV_NAME
  [[ -z "$ENV_NAME" ]] && break
  read -rp "  Description for $ENV_NAME: " ENV_DESC
  read -rp "  Required? (y/n) [y]: " ENV_REQ
  ENV_REQ=${ENV_REQ:-y}
  ENV_VARS+=("$ENV_NAME|$ENV_DESC|$ENV_REQ")
done

# Python deps
read -rp "Python dependencies (comma-separated, or enter for none): " DEPS_RAW

# Create directory
ITEM_DIR="items/${CATEGORY}/${ITEM_ID}"
mkdir -p "$ITEM_DIR"

# --- manifest.yaml ---
{
  echo "id: ${ITEM_ID}"
  echo "name: ${DISPLAY_NAME}"
  echo "description: >"
  echo "  ${DESCRIPTION}"
  echo "category: ${CATEGORY}"
  [[ -n "$SUBCATEGORY" ]] && echo "subcategory: ${SUBCATEGORY}"
  echo ""
  echo "files:"
  echo "  - src: ${SCRIPT_NAME}"
  echo "    dest: ${DEST_DIR}/${SCRIPT_NAME}"
  echo "  - src: AGENTS.md"
  echo "    dest: ${DEST_DIR}/AGENTS.md"
  echo ""

  # python_dependencies
  echo "python_dependencies:"
  if [[ -n "$DEPS_RAW" ]]; then
    IFS=',' read -ra DEPS <<< "$DEPS_RAW"
    for dep in "${DEPS[@]}"; do
      echo "  - \"$(echo "$dep" | xargs)\""
    done
  else
    echo "  []"
  fi
  echo ""

  # env_vars
  echo "env_vars:"
  if [[ ${#ENV_VARS[@]} -eq 0 ]]; then
    echo "  []"
  else
    for ev in "${ENV_VARS[@]}"; do
      IFS='|' read -r name desc req <<< "$ev"
      echo "  - name: ${name}"
      echo "    description: \"${desc}\""
      if [[ "$req" == "y" ]]; then
        echo "    required: true"
      else
        echo "    required: false"
      fi
    done
  fi
  echo ""

  echo "tags:"
  echo "  - ${ITEM_ID}"
  echo ""
  echo "tech_tags:"
  echo "  - python"
  echo ""
  echo "compatible_agents:"
  echo "  - any"
  echo ""
  echo "depends_on: []"
  echo "featured: false"
  echo ""
  echo "source:"
  echo "  type: original"
} > "${ITEM_DIR}/manifest.yaml"

# --- AGENTS.md ---
{
  echo "# ${DISPLAY_NAME}"
  echo ""
  echo "${DESCRIPTION}"
  echo ""
  echo "## Usage"
  echo ""
  echo '```bash'
  echo "python ${DEST_DIR}/${SCRIPT_NAME} --help"
  echo '```'
  echo ""
  if [[ ${#ENV_VARS[@]} -gt 0 ]]; then
    echo "## Environment Variables"
    echo ""
    for ev in "${ENV_VARS[@]}"; do
      IFS='|' read -r name desc req <<< "$ev"
      flag=""
      [[ "$req" == "y" ]] && flag=" (required)"
      echo "- \`${name}\`${flag}: ${desc}"
    done
    echo ""
  fi
  echo "## Output"
  echo ""
  echo "All commands output JSON to stdout. Errors output JSON to stderr with exit code 1."
} > "${ITEM_DIR}/AGENTS.md"

# --- Script skeleton ---
if [[ "$CATEGORY" == "skills" ]]; then
  {
    echo "# ${DISPLAY_NAME}"
    echo ""
    echo "${DESCRIPTION}"
    echo ""
    echo "## Steps"
    echo ""
    echo "1. TODO"
  } > "${ITEM_DIR}/${SCRIPT_NAME}"
else
  {
    echo '#!/usr/bin/env python3'
    echo "\"\"\"${DISPLAY_NAME} CLI.\"\"\""
    echo "import argparse"
    echo "import json"
    echo "import os"
    echo "import sys"
    echo ""
    echo ""
    echo "def main():"
    echo "    parser = argparse.ArgumentParser(description=\"${DISPLAY_NAME}\")"
    echo "    subparsers = parser.add_subparsers(dest=\"command\", help=\"Command to execute\")"
    echo ""
    echo "    # TODO: add subcommands here"
    echo "    # example_parser = subparsers.add_parser(\"example\", help=\"Example command\")"
    echo ""
    echo "    args = parser.parse_args()"
    echo "    if not args.command:"
    echo "        parser.print_help()"
    echo "        sys.exit(1)"
    echo ""
    echo ""
    echo 'if __name__ == "__main__":'
    echo "    main()"
  } > "${ITEM_DIR}/${SCRIPT_NAME}"
  chmod +x "${ITEM_DIR}/${SCRIPT_NAME}"
fi

echo ""
echo "Created ${ITEM_DIR}/"
echo "  - manifest.yaml"
echo "  - AGENTS.md"
echo "  - ${SCRIPT_NAME}"
echo ""
echo "Next steps:"
echo "  1. Edit ${ITEM_DIR}/${SCRIPT_NAME} — implement your commands"
echo "  2. Update ${ITEM_DIR}/AGENTS.md — document usage examples"
echo "  3. Validate: python scripts/validate-item.py ${ITEM_DIR}/"
echo "  4. Open a PR"
