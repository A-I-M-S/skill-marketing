#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/helpers.sh"

# ── Call AI endpoint (OpenAI-compatible) ─────────
# Usage: ai_chat "system prompt" "user prompt" [output_var_name]
# Sets output to the named variable, or prints to stdout.
ai_chat() {
    local system_prompt="$1"
    local user_prompt="$2"
    local output_var="${3:-}"

    local endpoint="${AI_ENDPOINT:-}"
    local api_key="${AI_API_KEY:-}"
    local model="${AI_MODEL:-gpt-4o}"

    if [[ -z "$endpoint" || -z "$api_key" ]]; then
        warn "AI_ENDPOINT or AI_API_KEY not set. Skipping AI call."
        return 1
    fi

    info "Calling $model via $endpoint ..."

    local response
    response=$(curl -s -w "\n%{http_code}" "$endpoint" \
        -H "Authorization: Bearer $api_key" \
        -H "Content-Type: application/json" \
        -d "$(cat <<EOF
{
    "model": "$model",
    "messages": [
        {"role": "system", "content": $(printf '%s' "$system_prompt" | jq -Rs .)},
        {"role": "user", "content": $(printf '%s' "$user_prompt" | jq -Rs .)}
    ],
    "temperature": 0.7,
    "max_tokens": 2048
}
EOF
    )")

    local http_code="${response##*$'\n'}"
    local body="${response%$'\n'*}"

    if [[ "$http_code" != "2"* ]]; then
        err "AI API error (HTTP $http_code): $(printf '%s' "$body" | head -c 500)"
        return 1
    fi

    local text
    text=$(printf '%s' "$body" | jq -r '.choices[0].message.content // empty')

    if [[ -z "$text" ]]; then
        err "Empty response from AI. Full body:"
        printf '%s\n' "$body" | head -c 300
        return 1
    fi

    if [[ -n "$output_var" ]]; then
        # Assign to variable in the caller's scope
        printf -v "$output_var" "%s" "$text"
    else
        printf "%s" "$text"
    fi

    ok "AI response received (${#text} chars)"
}

# ── Enhance content with AI ──────────────────────
# Takes a template file path, renders it, then optionally enhances with AI
ai_enhance() {
    local template_file="$1"
    local instructions="$2"
    local output_var="${3:-}"

    local base_content
    base_content=$(apply_template "$template_file")

    local system_prompt="You are a marketing content specialist for an AI business transformation consultancy targeting Singapore SMEs and enterprises. Keep the Singapore context front and centre. Reference relevant grants (PSG, EDG, SkillsFuture) where appropriate. Maintain a professional, authoritative tone. Do not add markdown formatting unless the original template uses it."

    local user_prompt="Here is a draft piece of content. $instructions\n\n---\n\n$base_content"

    ai_chat "$system_prompt" "$user_prompt" "$output_var"
}
