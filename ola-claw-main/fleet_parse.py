import sys, json

def fmt_tokens(n):
    if n >= 1_000_000: return f'{n/1_000_000:.1f}M'
    if n >= 1_000: return f'{n/1_000:.0f}K'
    return str(n)

d = json.load(sys.stdin)
uptime = d.get('uptime_seconds', 0)
hours = uptime // 3600
mins = (uptime % 3600) // 60
active = d.get('active_model', 'none')
active_key = d.get('active_key', '?')
budget = d.get('budget', {})
rpd_pct = int(budget.get('rpd_pct', 0) * 100)
rpm_peak_pct = int(budget.get('rpm_peak_pct', 0) * 100)
tpm_peak_pct = int(budget.get('tpm_peak_pct', 0) * 100)

models = d.get('models', {})

if active_key in ('primary', '?', None):
    prefix = None
else:
    prefix = active_key + ':'

# Filter models for active key
filtered = {}
for mname in sorted(models.keys()):
    if prefix is None:
        if ':' in mname:
            continue
    else:
        if not mname.startswith(prefix):
            continue
    filtered[mname] = models[mname]

# Compute totals for summary line
total_rpm_used = sum(m.get('rpm', {}).get('used', 0) for m in filtered.values())
total_rpm_bud = sum(m.get('rpm', {}).get('budget', 0) for m in filtered.values())
total_tpm_used = sum(m.get('tpm', {}).get('used', 0) for m in filtered.values())
total_tpm_bud = sum(m.get('tpm', {}).get('budget', 0) for m in filtered.values())
total_rpd_used = sum(m.get('rpd', {}).get('used', 0) for m in filtered.values())
total_rpd_bud = sum(m.get('rpd', {}).get('budget', 0) for m in filtered.values())

lines = []
lines.append(f'up {hours}h{mins}m | active: {active} (key: {active_key})')
lines.append(f'Daily: {rpd_pct}% RPD ({total_rpd_used}/{total_rpd_bud}) | now: {total_rpm_used}/{total_rpm_bud}rpm {fmt_tokens(total_tpm_used)}/{fmt_tokens(total_tpm_bud)}tpm | Peak: {rpm_peak_pct}% RPM, {tpm_peak_pct}% TPM')

for mname in sorted(filtered.keys()):
    m = filtered[mname]
    display_name = mname.split(':', 1)[-1] if ':' in mname else mname
    rpd_used = m.get('rpd', {}).get('used', 0)
    rpd_bud = m.get('rpd', {}).get('budget', 0)
    tpm_day = m.get('tpmDayTotal', 0)
    rpm_now = m.get('rpm', {}).get('used', 0)
    rpm_bud = m.get('rpm', {}).get('budget', 0)
    tpm_now = m.get('tpm', {}).get('used', 0)
    tpm_bud = m.get('tpm', {}).get('budget', 0)
    c429 = m.get('count429Today', 0)
    is_available = m.get('available', True)

    if display_name == active:
        tag = 'ACTIVE !!'
    elif not is_available:
        tag = 'EXHAUSTED'
    else:
        tag = 'ok'

    rpd_str = f'{rpd_used}/{rpd_bud}' if rpd_bud > 0 and rpd_bud != -1 else f'{rpd_used}/unlim'
    rpm_str = f'{rpm_now}/{rpm_bud}'
    tpm_str = f'{fmt_tokens(tpm_now)}/{fmt_tokens(tpm_bud)}'
    lines.append(f'  {display_name}: RPD {rpd_str} | TPM-day {fmt_tokens(tpm_day)} | now: {rpm_str}rpm {tpm_str}tpm | 429s:{c429} [{tag}]')

print('\n'.join(lines))
