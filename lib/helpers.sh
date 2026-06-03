#!/usr/bin/env bash
set -euo pipefail

# ── Colours ──────────────────────────────────────
export RED='\033[0;31m'
export GREEN='\033[0;32m'
export YELLOW='\033[1;33m'
export BLUE='\033[0;34m'
export CYAN='\033[0;36m'
export NC='\033[0m'

info()  { printf "${BLUE}%s${NC}\n" "$*"; }
ok()    { printf "${GREEN}✓ %s${NC}\n" "$*"; }
warn()  { printf "${YELLOW}⚠ %s${NC}\n" "$*"; }
err()   { printf "${RED}✗ %s${NC}\n" "$*"; }
header(){ printf "\n${CYAN}═══════════════════════════════════════════${NC}\n"; printf "${CYAN}  %s${NC}\n" "$*"; printf "${CYAN}═══════════════════════════════════════════${NC}\n"; }

# ── Load .env ────────────────────────────────────
load_env() {
    local env_file="${1:-.env}"
    if [[ -f "$env_file" ]]; then
        set -a
        source "$env_file"
        set +a
        ok "Loaded $env_file"
    else
        warn "No $env_file found. Copy .env.sample to .env and fill in your values."
    fi
}

# ── Validate required vars ───────────────────────
require_var() {
    local var_name="$1"
    if [[ -z "${!var_name:-}" ]]; then
        err "Missing required variable: $var_name"
        info "  Set it in .env or export it before running."
        exit 1
    fi
}

# ── Apply template (replace {{VAR}} with env values) ───
apply_template() {
    local input_file="$1"
    local output_file="${2:-}"
    local content

    content=$(<"$input_file")

    # Replace {{VAR}} with environment variable values
    while IFS='=' read -r key rest; do
        local var_name="$key"
        local var_value="${!var_name:-}"
        if [[ -n "$var_value" ]]; then
            content="${content//"{{${var_name}}}"/$var_value}"
        fi
    done < <(env | grep -o '^[^=]*')

    if [[ -n "$output_file" ]]; then
        printf "%s" "$content" > "$output_file"
        ok "Wrote $output_file"
    else
        printf "%s" "$content"
    fi
}

# ── Log with timestamp ──────────────────────────
log() {
    local msg="$1"
    local logdir="${SKILL_LOG_DIR:-logs}"
    mkdir -p "$logdir"
    printf "[%s] %s\n" "$(date '+%Y-%m-%d %H:%M:%S')" "$msg" >> "$logdir/skill.log"
}
