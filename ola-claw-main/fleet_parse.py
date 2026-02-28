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
active_key = d.get('active_key', 'primary')
budget = d.get('budget', {})
rpd_pct = int(budget.get('rpd_pct', 0) * 100)
rpm_peak_pct = int(budget.get('rpm_peak_pct', 0) * 100)
tpm_peak_pct = int(budget.get('tpm_peak_pct', 0) * 100)

models = d.get('models', {})
base_names = sorted(k for k in models if ':' not in k)

def aggregate(base):
    p = models.get(base, {})
    rpd_used = p.get('rpd', {}).get('used', 0)
    tpm_day = p.get('tpmDayTotal', 0)
    c429 = p.get('count429Today', 0)
    for mname, mdata in models.items():
        if ':' not in mname: continue
        kn, bn = mname.split(':', 1)
        if bn != base: continue
        rpd_used += mdata.get('rpd', {}).get('used', 0)
        tpm_day += mdata.get('tpmDayTotal', 0)
        c429 += mdata.get('count429Today', 0)
    return rpd_used, tpm_day, c429

lines = []
lines.append(f'up {hours}h{mins}m | active: {active} (key: {active_key})')

total_rpm_used = sum(models.get(b, {}).get('rpm', {}).get('used', 0) for b in base_names)
total_rpm_bud = sum(models.get(b, {}).get('rpm', {}).get('budget', 0) for b in base_names)
total_tpm_used = sum(models.get(b, {}).get('tpm', {}).get('used', 0) for b in base_names)
total_tpm_bud = sum(models.get(b, {}).get('tpm', {}).get('budget', 0) for b in base_names)
total_rpd_used = sum(aggregate(b)[0] for b in base_names)
total_rpd_bud = sum(models.get(b, {}).get('rpd', {}).get('budget', 0) for b in base_names)

lines.append(f'Daily: {rpd_pct}% RPD ({total_rpd_used}/{total_rpd_bud}) | now: {total_rpm_used}/{total_rpm_bud}rpm {fmt_tokens(total_tpm_used)}/{fmt_tokens(total_tpm_bud)}tpm | Peak: {rpm_peak_pct}% RPM, {tpm_peak_pct}% TPM')

for base in base_names:
    p = models.get(base, {})
    rpd_bud = p.get('rpd', {}).get('budget', 0)
    rpm_now = p.get('rpm', {}).get('used', 0)
    rpm_bud = p.get('rpm', {}).get('budget', 0)
    tpm_now = p.get('tpm', {}).get('used', 0)
    tpm_bud = p.get('tpm', {}).get('budget', 0)
    is_available = p.get('available', True)
    rpd_used, tpm_day, c429 = aggregate(base)

    if base == active: tag = 'ACTIVE !!'
    elif not is_available:
        st = p.get('status_tag', '')
        if st == 'COOLDOWN':
            remaining_m = p.get('cooldown_remaining_s', 0) // 60
            tag = f'COOLDOWN {remaining_m}m'
        else:
            tag = 'EXHAUSTED'
    else: tag = 'ok'

    rpd_str = f'{rpd_used}/{rpd_bud}' if rpd_bud > 0 else f'{rpd_used}/unlim'
    lines.append(f'  {base}: RPD {rpd_str} | TPM-day {fmt_tokens(tpm_day)} | now: {rpm_now}/{rpm_bud}rpm {fmt_tokens(tpm_now)}/{fmt_tokens(tpm_bud)}tpm | 429s:{c429} [{tag}]')

print('\n'.join(lines))
