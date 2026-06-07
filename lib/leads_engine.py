#!/usr/bin/env python3
import os
import sys
import csv
import json
import time
import urllib.request
import urllib.parse
from pathlib import Path

# --- Helpers to load env variables ---
def load_env(env_path=".env"):
    """Manually parse .env to avoid external dependency issues."""
    env_file = Path(env_path)
    if not env_file.exists():
        return
    with open(env_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, val = line.split("=", 1)
            key = key.strip()
            val = val.strip()
            if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                val = val[1:-1]
            os.environ[key] = val

load_env()

# --- Configurations ---
APOLLO_API_KEY = os.getenv("APOLLO_API_KEY", "")
HUNTER_API_KEY = os.getenv("HUNTER_API_KEY", "")
PDL_API_KEY = os.getenv("PDL_API_KEY", "")
SNOV_ID = os.getenv("SNOV_ID", "")
SNOV_API_KEY = os.getenv("SNOV_API_KEY", "")
CLAY_API_KEY = os.getenv("CLAY_API_KEY", "")
BREVO_API_KEY = os.getenv("BREVO_API_KEY", "")
BREVO_SENDER = os.getenv("BREVO_SENDER", "lily@aims-sg.com")
ATTIO_API_KEY = os.getenv("ATTIO_API_KEY", "")
CALENDLY_URL = os.getenv("CALENDLY_URL", "https://calendly.com/acwl/ac")

AI_ENDPOINT = os.getenv("AI_ENDPOINT", "https://api.openai.com/v1/chat/completions")
AI_API_KEY = os.getenv("AI_API_KEY", "")
AI_MODEL = os.getenv("AI_MODEL", "gpt-4o")

LEADS_PATH = Path("output/leads/leads.csv")
CONTACTED_PATH = Path("output/leads/contacted.csv")

# Ensure output directory exists
LEADS_PATH.parent.mkdir(parents=True, exist_ok=True)

# Target roles and location (excluding CTO)
TARGET_ROLES = ["CEO", "Founder", "Managing Director", "Owner", "Co-Founder"]
TARGET_LOCATION = "Singapore"

def is_cto(title):
    if not title:
        return False
    lower_title = title.lower()
    import re
    # Check for standalone "cto" as a word (with word boundaries)
    if re.search(r'\bcto\b', lower_title):
        return True
    # Check for specific CTO synonyms
    cto_phrases = [
        "chief technology officer", 
        "chief tech officer", 
        "chief technical officer", 
        "head of technology", 
        "director of technology", 
        "technology director", 
        "technology officer"
    ]
    for phrase in cto_phrases:
        if phrase in lower_title:
            return True
    return False

def log_msg(level, message):
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [{level}] {message}")
    log_file = Path("logs/marketing-combined.log")
    log_file.parent.mkdir(parents=True, exist_ok=True)
    with open(log_file, "a") as lf:
        lf.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [{level}] {message}\n")

# --- Local List Storage & Deduplication ---
def read_csv_leads(path):
    if not path.exists():
        return []
    leads = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("email"):
                leads.append(row)
    return leads

def write_csv_leads(path, leads):
    fieldnames = ["first_name", "last_name", "email", "company", "domain", "title"]
    cleaned_leads = []
    for lead in leads:
        cleaned = {k: lead.get(k, "") for k in fieldnames}
        cleaned_leads.append(cleaned)

    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned_leads)

def get_all_known_emails():
    pending = [l["email"].lower() for l in read_csv_leads(LEADS_PATH)]
    contacted = [l["email"].lower() for l in read_csv_leads(CONTACTED_PATH)]
    return set(pending + contacted)

def add_new_leads_to_pool(new_leads):
    """Integrates new leads, deduplicating against pending (leads.csv) and historic (contacted.csv) databases."""
    known_emails = get_all_known_emails()
    added_count = 0
    leads_to_append = []

    for lead in new_leads:
        email = lead.get("email", "").strip().lower()
        if not email or "@" not in email:
            continue
        if email in known_emails:
            continue
        leads_to_append.append(lead)
        known_emails.add(email)
        added_count += 1

    if leads_to_append:
        existing = read_csv_leads(LEADS_PATH)
        existing.extend(leads_to_append)
        write_csv_leads(LEADS_PATH, existing)

    log_msg("INFO", f"Added {added_count} brand-new leads to {LEADS_PATH.name}")
    return added_count

# --- API Request Helper ---
def make_request(url, method="GET", headers=None, data=None):
    if headers is None:
        headers = {}
    req_data = None
    if data:
        if isinstance(data, dict) or isinstance(data, list):
            req_data = json.dumps(data).encode("utf-8")
            headers["Content-Type"] = "application/json"
        else:
            req_data = data.encode("utf-8")

    req = urllib.request.Request(url, data=req_data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            status = response.status
            body = response.read().decode("utf-8")
            return status, body
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8") if e.fp else ""
        return e.code, body
    except Exception as e:
        return 500, str(e)

# --- Lead Providers (Step 1a: Harvest) ---

# 1. Apollo.io Search Client
def fetch_apollo_leads(count=50):
    if not APOLLO_API_KEY:
        log_msg("WARN", "Apollo API key not configured.")
        return None, "Skipped: Missing API key"

    log_msg("INFO", "Querying Apollo.io Mixed People Search API...")
    url = "https://api.apollo.io/api/v1/mixed_people/api_search"
    headers = {
        "x-api-key": APOLLO_API_KEY,
        "accept": "application/json"
    }
    payload = {
        "person_locations": [TARGET_LOCATION],
        "person_titles": TARGET_ROLES,
        "per_page": min(count, 100)
    }

    status, body = make_request(url, "POST", headers, payload)
    if status != 200:
        log_msg("ERROR", f"Apollo Search failed (HTTP {status}): {body[:300]}")
        return None, f"HTTP Error {status}"

    try:
        data = json.loads(body)
        raw_people = data.get("people", [])
        leads = []
        for p in raw_people:
            email = p.get("email")
            org = p.get("organization", {})
            domain = org.get("primary_domain", "")
            company = org.get("name", "")
            
            leads.append({
                "first_name": p.get("first_name", ""),
                "last_name": p.get("last_name", ""),
                "email": email or "",
                "company": company,
                "domain": domain,
                "title": p.get("title", "")
            })
        log_msg("OK", f"Apollo returned {len(leads)} potential leads.")
        return leads, None
    except Exception as e:
        log_msg("ERROR", f"Failed to parse Apollo response: {str(e)}")
        return None, "Parsing Error"

# 2. People Data Labs Search Client
def fetch_pdl_leads(count=50):
    if not PDL_API_KEY:
        log_msg("WARN", "PDL API key not configured.")
        return None, "Skipped: Missing API key"

    log_msg("INFO", "Querying People Data Labs Person Search API...")
    url = "https://api.peopledatalabs.com/v5/person/search"
    headers = {
        "X-Api-Key": PDL_API_KEY,
        "accept": "application/json"
    }

    roles_str = ", ".join([f"'{r.lower()}'" for r in TARGET_ROLES])
    sql_query = f"SELECT first_name, last_name, work_email, job_company_name, job_company_website, job_title FROM person WHERE location_country='singapore' AND job_title_role IN ({roles_str}) AND work_email IS NOT NULL"
    
    params = urllib.parse.urlencode({
        "sql": sql_query,
        "size": min(count, 100)
    })
    
    status, body = make_request(f"{url}?{params}", "GET", headers)
    if status != 200:
        log_msg("ERROR", f"PDL Search failed (HTTP {status}): {body[:300]}")
        return None, f"HTTP Error {status}"

    try:
        data = json.loads(body)
        raw_records = data.get("data", [])
        leads = []
        for r in raw_records:
            website = r.get("job_company_website", "")
            domain = website.replace("http://", "").replace("https://", "").replace("www.", "").split("/")[0] if website else ""
            leads.append({
                "first_name": r.get("first_name", ""),
                "last_name": r.get("last_name", ""),
                "email": r.get("work_email", ""),
                "company": r.get("job_company_name", ""),
                "domain": domain,
                "title": r.get("job_title", "")
            })
        log_msg("OK", f"PDL returned {len(leads)} potential leads.")
        return leads, None
    except Exception as e:
        log_msg("ERROR", f"Failed to parse PDL response: {str(e)}")
        return None, "Parsing Error"

# 3. Hunter Domain Search Client
def fetch_hunter_leads(count=50):
    if not HUNTER_API_KEY:
        log_msg("WARN", "Hunter API key not configured.")
        return None, "Skipped: Missing API key"

    target_domains = ["viki.com", "razer.com", "grab.com", "sea.com", "shopback.sg", "propertyguru.com.sg", "hometogo.sg"]
    leads = []
    
    log_msg("INFO", f"Querying Hunter.io Domain Search for local domains...")
    for domain in target_domains:
        if len(leads) >= count:
            break
            
        url = f"https://api.hunter.io/v2/domain-search?domain={domain}&api_key={HUNTER_API_KEY}"
        status, body = make_request(url, "GET")
        if status != 200:
            log_msg("ERROR", f"Hunter failed for {domain} (HTTP {status}). Moving on.")
            continue

        try:
            data = json.loads(body)
            raw_emails = data.get("data", {}).get("emails", [])
            for e in raw_emails:
                title = e.get("position", "")
                if is_cto(title) or any(t in (title or "").lower() for t in ["developer", "engineer"]):
                    continue
                    
                leads.append({
                    "first_name": e.get("first_name", ""),
                    "last_name": e.get("last_name", ""),
                    "email": e.get("value", ""),
                    "company": domain.split(".")[0].capitalize(),
                    "domain": domain,
                    "title": title or "Executive"
                })
        except Exception as err_msg:
            log_msg("ERROR", f"Error parsing Hunter response for {domain}: {str(err_msg)}")
            
    log_msg("OK", f"Hunter returned {len(leads)} potential leads.")
    return leads if leads else None, None if leads else "No leads found"

# 4. Snov.io Domain Search Client
def fetch_snov_leads(count=50):
    if not SNOV_ID or not SNOV_API_KEY:
        log_msg("WARN", "Snov credentials not configured.")
        return None, "Skipped: Missing credentials"

    log_msg("INFO", "Authenticating with Snov.io API...")
    auth_url = "https://api.snov.io/v1/oauth/access_token"
    auth_payload = {
        "grant_type": "client_credentials",
        "client_id": SNOV_ID,
        "client_secret": SNOV_API_KEY
    }
    
    status, body = make_request(auth_url, "POST", data=auth_payload)
    if status != 200:
        log_msg("ERROR", f"Snov authentication failed (HTTP {status}): {body}")
        return None, f"Auth Error {status}"

    try:
        token_data = json.loads(body)
        access_token = token_data.get("access_token")
    except Exception as e:
        log_msg("ERROR", f"Snov token parse error: {str(e)}")
        return None, "Token Parse Error"

    target_domains = ["singlife.com", "smecentre-asme.sg", "ninjaexpress.co", "carousell.sg"]
    leads = []
    headers = {"Authorization": f"Bearer {access_token}"}

    log_msg("INFO", "Querying Snov.io for Singapore domain emails...")
    for domain in target_domains:
        if len(leads) >= count:
            break
            
        start_url = "https://api.snov.io/v2/domain-search/domain-emails/start"
        payload = {"domain": domain}
        
        status, body = make_request(start_url, "POST", headers, payload)
        if status != 200:
            continue

        try:
            res_data = json.loads(body)
            emails = res_data.get("emails", [])
            for e in emails:
                leads.append({
                    "first_name": e.get("firstName", ""),
                    "last_name": e.get("lastName", ""),
                    "email": e.get("email", ""),
                    "company": domain.split(".")[0].capitalize(),
                    "domain": domain,
                    "title": e.get("position", "Manager")
                })
        except Exception:
            pass

    log_msg("OK", f"Snov returned {len(leads)} potential leads.")
    return leads if leads else None, None if leads else "No leads found"

# 5. Clay Table Client / Mock
def fetch_clay_leads(count=50):
    if not CLAY_API_KEY:
        log_msg("WARN", "Clay API Key not configured.")
        return None, "Skipped: Missing API key"

    log_msg("INFO", "Querying Clay.com REST tables...")
    clay_table_id = os.getenv("CLAY_TABLE_ID", "")
    if not clay_table_id:
        log_msg("WARN", "CLAY_TABLE_ID not set in .env. Returning simulated sample lead.")
        return [{
            "first_name": "Marcus",
            "last_name": "Tan",
            "email": "marcus.tan@sg-retail-solutions.com",
            "company": "SG Retail Solutions",
            "domain": "sg-retail-solutions.com",
            "title": "Managing Director"
        }], None

    url = f"https://api.clay.com/v1/tables/{clay_table_id}/rows"
    headers = {"X-Api-Key": CLAY_API_KEY}
    status, body = make_request(url, "GET", headers)
    if status != 200:
        return None, f"Clay Error {status}"

    try:
        data = json.loads(body)
        rows = data.get("rows", [])
        leads = []
        for r in rows:
            vals = r.get("values", {})
            leads.append({
                "first_name": vals.get("first_name", vals.get("First Name", "")),
                "last_name": vals.get("last_name", vals.get("Last Name", "")),
                "email": vals.get("email", vals.get("Email", "")),
                "company": vals.get("company", vals.get("Company", "")),
                "domain": vals.get("domain", vals.get("Domain", "")),
                "title": vals.get("title", vals.get("Title", ""))
            })
        return leads, None
    except Exception as e:
        return None, f"Parse Error: {str(e)}"

# --- Fallback Generation Chain ---
def generate_new_leads(target_count=200):
    log_msg("INFO", f"Triggering lead generation pipeline for {target_count} leads...")
    providers = [
        ("Apollo", fetch_apollo_leads),
        ("People Data Labs", fetch_pdl_leads),
        ("Hunter", fetch_hunter_leads),
        ("Snov", fetch_snov_leads),
        ("Clay", fetch_clay_leads)
    ]

    total_added = 0
    for name, fetch_func in providers:
        if total_added >= target_count:
            break

        log_msg("INFO", f"=== Attempting Provider: {name} ===")
        try:
            leads, err_reason = fetch_func(target_count - total_added)
            if leads:
                added = add_new_leads_to_pool(leads)
                total_added += added
                log_msg("OK", f"Provider {name} successfully added {added} deduplicated leads.")
            else:
                log_msg("WARN", f"Provider {name} failed or skipped: {err_reason or 'No leads returned'}")
        except Exception as e:
            log_msg("ERROR", f"Provider {name} crashed with exception: {str(e)}")

    log_msg("OK", f"Lead generation run complete. Total brand-new leads harvested: {total_added}")
    return total_added

# --- AI Domain Research and Personalizer ---
def extract_domain_trade(domain):
    """Pings the homepage or uses LLM to identify the company's business model."""
    if not domain:
        return "General Business"

    log_msg("INFO", f"Researching trade category for website: {domain}...")
    try:
        url = f"http://{domain}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=4) as conn:
            html = conn.read().decode("utf-8", errors="ignore")
            title_start = html.find("<title>")
            title = ""
            if title_start != -1:
                title_end = html.find("</title>", title_start)
                title = html[title_start + 7:title_end].strip()
            
            desc_start = html.find('name="description" content="')
            desc = ""
            if desc_start != -1:
                desc_end = html.find('"', desc_start + 28)
                desc = html[desc_start + 28:desc_end].strip()
                
            summary = f"Title: {title}. Desc: {desc}"
            if len(summary) > 20:
                log_msg("OK", f"Scraped site header: {summary[:100]}...")
                return summary[:500]
    except Exception:
        pass
        
    return "Domain lookup timed out or restricted. Fallback to generic sector matching."

def generate_personalized_pitch(lead, trade_info):
    """Calls OpenAI-compatible LLM to write a targeted B2B pitch."""
    if not AI_API_KEY:
        log_msg("WARN", "AI_API_KEY not configured. Falling back to static template.")
        return f"Hi {lead['first_name']},\n\nI noticed {lead['company']} is doing great work. At AIMS, we help Singapore SMEs transition into autonomous, high-efficiency AI agents. I would love to schedule a quick chat to explore how this applies to you.\n\nBest,\nLily"

    system_prompt = (
        "You are Lily, a Business Growth Executive at AIMS (aims-sg.com). "
        "AIMS is a premier AI consultancy in Singapore that specializes in helping SMEs perform 'Agentic Business Transformation' (integrating custom AI Agents and autonomous workflow automation to cut overhead and scale operations with 0$ ad spend). "
        "Your tone must be highly professional, consultative, and direct. Avoid generic marketing hype. Keep the pitch concise (under 150 words)."
    )
    
    user_prompt = (
        f"Draft a highly tailored cold outreach email targeting:\n"
        f"Name: {lead['first_name']} {lead['last_name']}\n"
        f"Job Title: {lead['title']}\n"
        f"Company: {lead['company']}\n"
        f"Website: {lead['domain']}\n"
        f"Company Trade/Sector Details: {trade_info}\n\n"
        f"Requirements:\n"
        f"1. Explain how AIMS can specifically benefit their exact trade or solve their bottlenecks with AI Agents.\n"
        f"2. Conclude with a clear Call-to-Action to schedule a consultation with our Tech Founder using this Calendly link: {CALENDLY_URL}\n"
        f"3. Output only the email Subject Line and Body."
    )

    log_msg("INFO", f"Generating AI customized pitch for {lead['email']}...")
    payload = {
        "model": AI_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }
    
    headers = {
        "Authorization": f"Bearer {AI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    status, body = make_request(AI_ENDPOINT, "POST", headers, payload)
    if status != 200:
        log_msg("ERROR", f"AI API generation failed: {body[:300]}")
        return "Error generating AI pitch"

    try:
        data = json.loads(body)
        pitch = data["choices"][0]["message"]["content"].strip()
        return pitch
    except Exception as e:
        log_msg("ERROR", f"Failed to parse AI response: {str(e)}")
        return "Error parsing AI pitch"

# --- CRM Upsert (Attio) ---
def upsert_to_attio(lead, status_label="contacted"):
    if not ATTIO_API_KEY:
        log_msg("WARN", "Attio API Key not configured. Skipping CRM sync.")
        return False

    url = "https://api.attio.com/v2/objects/people/records?matching_attribute=email_addresses"
    headers = {
        "Authorization": f"Bearer {ATTIO_API_KEY}",
        "Content-Type": "application/json"
    }

    # Attempt to upsert standard record
    payload = {
        "data": {
            "values": {
                "email_addresses": [{"email_address": lead["email"]}],
                "name": {
                    "first_name": lead["first_name"],
                    "last_name": lead["last_name"],
                    "full_name": f"{lead['first_name']} {lead['last_name']}".strip()
                },
                "company": lead["company"],
                "status": status_label
            }
        }
    }

    log_msg("INFO", f"Upserting {lead['email']} to Attio CRM with status: {status_label}...")
    status, body = make_request(url, "PUT", headers, payload)
    
    if status not in [200, 201]:
        log_msg("WARN", f"Attio sync failed with full payload (HTTP {status}). Falling back to simple schema...")
        fallback_payload = {
            "data": {
                "values": {
                    "email_addresses": [{"email_address": lead["email"]}],
                    "name": {
                        "first_name": lead["first_name"],
                        "last_name": lead["last_name"],
                        "full_name": f"{lead['first_name']} {lead['last_name']}".strip()
                    }
                }
            }
        }
        status, body = make_request(url, "PUT", headers, fallback_payload)
        
    if status in [200, 201]:
        log_msg("OK", f"Successfully synced contact with Attio CRM.")
        return True
    else:
        log_msg("ERROR", f"Attio CRM upsert completely failed (HTTP {status}): {body}")
        return False

# --- Email Delivery (Brevo) ---
def send_email_via_brevo(recipient_email, recipient_name, subject, html_content):
    if not BREVO_API_KEY:
        log_msg("ERROR", "Brevo API key not configured. Cannot deliver email.")
        return False

    url = "https://api.brevo.com/v3/smtp/email"
    headers = {
        "api-key": BREVO_API_KEY,
        "content-type": "application/json"
    }

    payload = {
        "sender": {"email": BREVO_SENDER, "name": "Lily @ AIMS"},
        "to": [{"email": recipient_email, "name": recipient_name}],
        "subject": subject,
        "textContent": html_content
    }

    log_msg("INFO", f"Sending email via Brevo to {recipient_email}...")
    status, body = make_request(url, "POST", headers, payload)
    if status == 201 or status == 200:
        log_msg("OK", "Email sent successfully.")
        return True
    else:
        log_msg("ERROR", f"Brevo email sending failed (HTTP {status}): {body}")
        return False

# --- Orchestrated Daily Run Engine ---
def execute_outbound_cycle(count=200, mode="draft-only", test_address=None):
    log_msg("INFO", f"Starting marketing outbound cycle (Count limit: {count}, Mode: {mode})...")
    
    # Step 2: Read strictly from pending list (leads.csv)
    pending_leads = read_csv_leads(LEADS_PATH)
    
    if not pending_leads:
        log_msg("ERROR", f"The pending list ({LEADS_PATH.name}) is completely empty. Run Step 1 to harvest/import leads first!")
        return

    leads_to_process = pending_leads[:count]
    remaining_leads = pending_leads[count:]

    processed_leads = []
    drafts = []

    for lead in leads_to_process:
        log_msg("INFO", f"--------------------------------------------------")
        log_msg("INFO", f"Processing Prospect: {lead['first_name']} {lead['last_name']} ({lead['email']})")

        # 1. Trade Research
        trade_info = extract_domain_trade(lead["domain"])

        # 2. Personalized AI Pitch
        raw_pitch = generate_personalized_pitch(lead, trade_info)
        
        # Parse subject and body from AI output
        subject = f"AI Agent Transformation for {lead['company']}"
        body = raw_pitch
        if "Subject:" in raw_pitch:
            lines = raw_pitch.split("\n")
            for l in lines:
                if l.startswith("Subject:"):
                    subject = l.replace("Subject:", "").strip()
                    body = raw_pitch.replace(l, "").strip()
                    break

        drafts.append({
            "email": lead["email"],
            "name": f"{lead['first_name']} {lead['last_name']}",
            "company": lead["company"],
            "subject": subject,
            "body": body
        })

        # 3. CRM Sync (Attio)
        if mode != "draft-only":
            upsert_to_attio(lead, status_label="contacted")

        # 4. Delivery Control
        if mode == "send":
            send_email_via_brevo(lead["email"], f"{lead['first_name']} {lead['last_name']}", subject, body)
        elif mode == "test" and test_address:
            log_msg("INFO", f"Routing test email to: {test_address} instead of {lead['email']}")
            send_email_via_brevo(test_address, f"TEST: {lead['first_name']}", f"[TEST-MODE] {subject}", body)

        processed_leads.append(lead)

    # In send or test modes, modify the list to prevent repeat emailing
    if mode in ["send", "test"]:
        # Append processed leads to contacted.csv (archive)
        contacted_leads = read_csv_leads(CONTACTED_PATH)
        contacted_leads.extend(processed_leads)
        write_csv_leads(CONTACTED_PATH, contacted_leads)

        # Remove processed rows from leads.csv
        write_csv_leads(LEADS_PATH, remaining_leads)
        log_msg("OK", f"Successfully updated CSV databases. Handled {len(processed_leads)} contacts.")
    else:
        # Save drafts locally for human-review
        draft_file = Path("output/leads/drafts_today.json")
        draft_file.parent.mkdir(parents=True, exist_ok=True)
        with open(draft_file, "w", encoding="utf-8") as df:
            json.dump(drafts, df, indent=2)
        log_msg("OK", f"Draft-only run completed. Saved {len(drafts)} drafts to {draft_file}")

if __name__ == "__main__":
    print("Leads Engine successfully initialized.")
