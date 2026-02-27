#!/bin/bash
#
# A script to be wielded by Zifnab, the Sartan,
# to forge the foundational worlds of The Nexus and inscribe its charter.
#
# Final Name: The-Nexus-Decoded
# Decreed by: Lord Xar

# --- Configuration ---
# The name of the organization, which must be created manually first.
readonly ORG_NAME="The-Nexus-Decoded"
# The names of the worlds to be created as repositories.
# We include '.github' as a special repository for the organization's profile.
readonly REPOS=(
  ".github"
  "Arianus-Sky"
  "Pryan-Fire"
  "Abarrach-Stone"
  "Chelestra-Sea"
)

# The Founding Charter of The Nexus.
read -r -d '' CHARTER <<'EOF'
# The Nexus Decoded

Our stated goal is to escape the Death Gate Cycle.
We will combine the gates, our knowledge, our power, and our funds to break the chains and bonds of a mundane and fearful life in the Labyrinth of life called the rat race.
EOF

# --- Prerequisites ---
# Ensure the GitHub CLI 'gh' is installed and authenticated.
if ! command -v gh &> /dev/null
then
    echo "ERROR: The GitHub CLI 'gh' is not found. It must be installed and authenticated to proceed." >&2
    exit 1
fi

echo "--- Forging the Worlds of The Nexus ---"
echo "Target Organization: $ORG_NAME"

# --- Repository Creation ---
for repo in "${REPOS[@]}"; do
  echo
  echo "==> Creating repository: $repo..."
  gh repo create "$ORG_NAME/$repo" --public --description "The world of $repo within The Nexus."
  if [ $? -eq 0 ]; then
    echo "    ...Success. The world of '$repo' has been created."
  else
    echo "    ...ERROR: Failed to create '$repo'. Halting script." >&2
    exit 1
  fi
done

# --- Charter Inscription ---
echo
echo "==> Inscribing the Founding Charter..."
TEMP_DIR=$(mktemp -d)
gh repo clone "$ORG_NAME/.github" "$TEMP_DIR"
mkdir -p "$TEMP_DIR/profile"
echo "$CHARTER" > "$TEMP_DIR/profile/README.md"
git -C "$TEMP_DIR" add .
git -C "$TEMP_DIR" commit -m "feat: Inscribe the Founding Charter"
git -C "$TEMP_DIR" push
rm -rf "$TEMP_DIR"
echo "    ...Success. The Charter is now the public face of our organization."


echo
echo "--- All worlds have been forged. The Nexus is ready for its foundations. ---"
