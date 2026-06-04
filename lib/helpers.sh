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

MARKETING_LOG_FILE="${MARKETING_LOG_FILE:-logs/marketing-combined.log}"

# ── Load .env ────────────────────────────────────
load_env() {
    local env_file="${1:-${MARKETING_ENV_FILE:-.env}}"
    if [[ -f "$env_file" ]]; then
        local line key value
        while IFS= read -r line || [[ -n "$line" ]]; do
            line="${line%$'\r'}"
            [[ -z "$line" || "$line" == \#* ]] && continue
            [[ "$line" != *=* ]] && continue

            key="${line%%=*}"
            value="${line#*=}"

            if [[ ! "$key" =~ ^[A-Za-z_][A-Za-z0-9_]*$ ]]; then
                warn "Skipping invalid env key: $key"
                continue
            fi

            if [[ "${value:0:1}" == '"' && "${value: -1}" == '"' ]]; then
                value="${value:1:${#value}-2}"
            elif [[ "${value:0:1}" == "'" && "${value: -1}" == "'" ]]; then
                value="${value:1:${#value}-2}"
            fi

            export "$key=$value"
        done < "$env_file"
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
    local level="${1:-INFO}"
    shift || true
    local msg="$*"
    mkdir -p "$(dirname "$MARKETING_LOG_FILE")"
    printf "[%s] [%s] %s\n" "$(date '+%Y-%m-%d %H:%M:%S')" "$level" "$msg" >> "$MARKETING_LOG_FILE"
}

log_info() { log "INFO" "$*"; }
log_ok() { log "OK" "$*"; }
log_warn() { log "WARN" "$*"; }
log_error() { log "ERROR" "$*"; }

write_status() {
    local status_file="${MARKETING_STATUS_FILE:-output/status/latest-status.md}"
    local status="${1:-unknown}"
    local summary="${2:-No summary provided.}"
    mkdir -p "$(dirname "$status_file")"
    cat > "$status_file" <<STATUS
# Marketing Automation Status

Last checked: $(date '+%Y-%m-%d %H:%M:%S')

## Process
Status: $status
Runner: PM2-compatible Bash daemon
Combined log: $MARKETING_LOG_FILE

## Summary
$summary

## Review Required
- Review all generated content before publishing.
- Review all outreach drafts before sending.
- Fill in Share of Model results manually after querying AI engines.

## Agent Review
Use \`checklists/agent-log-review.md\` with this file and the combined log.
STATUS
}
