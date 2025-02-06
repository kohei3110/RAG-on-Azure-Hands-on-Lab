#!/usr/bin/env bash

# create .env
cat <<-EOF > .devcontainer/.env
GIT_NAME=$(git config --get user.name)
GIT_EMAIL=$(git config --get user.email)
EOF