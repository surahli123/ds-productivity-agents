# Security Logs Analysis Log

## Overview

**Dataset:** 7 CSV files representing a security operations dataset
**Tool:** Python sqlite3 module
**Date:** 2026-03-20

### Data Summary

| Table | Rows | Description |
|-------|------|-------------|
| organizations | 120 | Companies by industry and country |
| users | 1,500 | Users with roles (Admin, Analyst, Employee) |
| systems | 600 | IT systems with OS type and criticality level |
| security_incidents | 500 | Incidents (Malware, Data Breach, Unauthorized Access) |
| incident_systems | 500 | Many-to-many link between incidents and systems |
| login_logs | 6,000 | Login attempts with success/failure status |
| network_events | 5,000 | Network events by type and severity |

### Schema Relationships

- `organizations.org_id` is the root -- users, systems, and incidents all belong to an org
- `incident_systems` links incidents to the systems they affected (junction table)
- `login_logs` links to users; `network_events` links to systems
- No direct FK from login_logs to systems or from network_events to users

---

## Step 1: Load Data into SQLite

**What I did:** Created a SQLite database with 7 tables matching the CSV schemas, with appropriate primary keys and foreign key constraints. Loaded all CSV data using Python's `csv` module and `sqlite3`.

**Decision:** Used TEXT types for all columns since the CSV data is string-formatted (dates as `YYYY-MM-DD`, IDs as prefixed strings like `U0001`). SQLite's type affinity handles this cleanly.

**SQL (table creation example):**

```sql
CREATE TABLE security_incidents (
    incident_id TEXT PRIMARY KEY,
    org_id TEXT,
    incident_type TEXT,
    discovered_date TEXT,
    severity TEXT,
    FOREIGN KEY (org_id) REFERENCES organizations(org_id)
);

CREATE TABLE incident_systems (
    incident_id TEXT,
    system_id TEXT,
    PRIMARY KEY (incident_id, system_id),
    FOREIGN KEY (incident_id) REFERENCES security_incidents(incident_id),
    FOREIGN KEY (system_id) REFERENCES systems(system_id)
);
```

**Result:** All 7 tables loaded successfully. Row counts verified against source files.

---

## Step 2: Incident Types and Severity Distribution

**What I did:** Queried `security_incidents` to find the frequency of each incident type and how severity breaks down within each type.

### Query: Incident Type Counts

```sql
SELECT incident_type, COUNT(*) as count
FROM security_incidents
GROUP BY incident_type
ORDER BY count DESC;
```

**Result:**

| Incident Type | Count |
|---------------|-------|
| Malware | 185 (37%) |
| Data Breach | 166 (33.2%) |
| Unauthorized Access | 149 (29.8%) |

### Query: Incident Type x Severity Cross-Tab

```sql
SELECT
    incident_type,
    severity,
    COUNT(*) as count
FROM security_incidents
GROUP BY incident_type, severity
ORDER BY incident_type,
    CASE severity
        WHEN 'Critical' THEN 1 WHEN 'High' THEN 2
        WHEN 'Medium' THEN 3 WHEN 'Low' THEN 4
    END;
```

**Result:**

| Incident Type | Critical | High | Medium | Low |
|---------------|----------|------|--------|-----|
| Data Breach | 49 | 32 | 32 | 53 |
| Malware | 48 | 49 | 45 | 43 |
| Unauthorized Access | 43 | 39 | 34 | 33 |

### Query: Overall Severity Distribution

```sql
SELECT severity, COUNT(*) as count,
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM security_incidents), 1) as pct
FROM security_incidents
GROUP BY severity
ORDER BY CASE severity
    WHEN 'Critical' THEN 1 WHEN 'High' THEN 2
    WHEN 'Medium' THEN 3 WHEN 'Low' THEN 4
END;
```

**Result:**

| Severity | Count | % |
|----------|-------|---|
| Critical | 140 | 28.0% |
| High | 120 | 24.0% |
| Medium | 111 | 22.2% |
| Low | 129 | 25.8% |

**Observations:**
- Malware is the most common incident type (37%), followed by Data Breach (33%) and Unauthorized Access (30%). The distribution is relatively even -- no single type dominates overwhelmingly.
- Severity is nearly uniformly distributed across all four levels (22-28%). This suggests the severity assignment may be random/synthetic, or the org triages incidents across the spectrum consistently.
- Data Breach has a U-shaped severity profile: more Critical (49) and Low (53) than Medium (32) or High (32). This could indicate a bimodal pattern where breaches are either serious or minor, with fewer in the middle.
- Malware has the flattest distribution across severities, suggesting it spans the full range of impact.

---

## Step 3: Users with Most Failed Logins

**What I did:** Joined `login_logs` with `users` to identify which users had the highest failed login counts, and computed failure rates to distinguish "high-volume users who sometimes fail" from "users who almost always fail."

### Query: Top 15 Users by Failed Logins

```sql
SELECT
    l.user_id,
    u.role,
    u.org_id,
    COUNT(*) as failed_logins,
    (SELECT COUNT(*) FROM login_logs l2 WHERE l2.user_id = l.user_id) as total_logins
FROM login_logs l
JOIN users u ON l.user_id = u.user_id
WHERE l.status = 'Failed'
GROUP BY l.user_id
ORDER BY failed_logins DESC
LIMIT 15;
```

**Result:**

| User | Role | Org | Failed | Total | Fail Rate |
|------|------|-----|--------|-------|-----------|
| U1340 | Analyst | ORG001 | 8 | 11 | 72.7% |
| U1281 | Admin | ORG029 | 8 | 10 | 80.0% |
| U0940 | Admin | ORG057 | 8 | 11 | 72.7% |
| U0367 | Employee | ORG084 | 8 | 9 | 88.9% |
| U1447 | Admin | ORG028 | 7 | 12 | 58.3% |
| U1427 | Admin | ORG086 | 7 | 9 | 77.8% |
| U1410 | Employee | ORG082 | 7 | 10 | 70.0% |
| U1376 | Admin | ORG038 | 7 | 9 | 77.8% |
| U1326 | Admin | ORG018 | 7 | 10 | 70.0% |
| U0540 | Analyst | ORG018 | 7 | 8 | 87.5% |
| U0279 | Analyst | ORG036 | 7 | 7 | 100.0% |
| U0061 | Analyst | ORG006 | 7 | 12 | 58.3% |
| U0051 | Employee | ORG079 | 7 | 9 | 77.8% |
| U1491 | Employee | ORG040 | 6 | 6 | 100.0% |
| U1453 | Employee | ORG034 | 6 | 10 | 60.0% |

### Query: Failed Logins by Role

```sql
SELECT
    u.role,
    COUNT(*) as failed_logins,
    COUNT(DISTINCT l.user_id) as unique_users,
    ROUND(COUNT(*) * 1.0 / COUNT(DISTINCT l.user_id), 1) as avg_fails_per_user
FROM login_logs l
JOIN users u ON l.user_id = u.user_id
WHERE l.status = 'Failed'
GROUP BY u.role
ORDER BY failed_logins DESC;
```

**Result:**

| Role | Total Failed | Unique Users | Avg per User |
|------|-------------|--------------|--------------|
| Admin | 1,008 | 432 | 2.3 |
| Analyst | 980 | 423 | 2.3 |
| Employee | 972 | 430 | 2.3 |

### Query: Overall Login Success/Failure Rate

```sql
SELECT
    status, COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM login_logs), 1) as pct
FROM login_logs
GROUP BY status;
```

**Result:** Failed: 2,960 (49.3%) | Success: 3,040 (50.7%)

**Observations:**
- The overall failure rate is 49.3% -- nearly 1 in 2 login attempts fail. This is abnormally high for a real production environment (typical is 5-15%), suggesting either (a) synthetic/randomized data, (b) an active brute-force campaign, or (c) severe usability issues with auth.
- Two users (U0279, U1491) have a 100% failure rate -- every single login attempt failed. These are strong candidates for compromised or locked accounts.
- U0367 (Employee, ORG084) has an 88.9% failure rate over 9 attempts -- another red flag.
- Failure rates are perfectly uniform across roles (~2.3 failed per user, ~same total across Admin/Analyst/Employee). In real data, Admins often have lower failure rates (more experienced) or higher (targeted attacks). This uniformity is another signal the data may be synthetically generated.
- The top failed-login users come from many different organizations -- there is no single org with a cluster of failing users, suggesting no org-level credential issue.

---

## Step 4: Most Vulnerable Systems (Incidents Joined with Systems)

**What I did:** Joined `incident_systems` with `systems` and `security_incidents` to find which systems are most frequently involved in incidents, and sliced the data by OS type and criticality level.

### Query: Top 15 Systems by Incident Count

```sql
SELECT
    s.system_id, s.os_type, s.criticality, s.org_id, o.industry,
    COUNT(DISTINCT si.incident_id) as incident_count
FROM incident_systems isys
JOIN systems s ON isys.system_id = s.system_id
JOIN security_incidents si ON isys.incident_id = si.incident_id
JOIN organizations o ON s.org_id = o.org_id
GROUP BY s.system_id
ORDER BY incident_count DESC
LIMIT 15;
```

**Result:**

| System | OS | Criticality | Org | Industry | Incidents |
|--------|------|-------------|------|------------|-----------|
| S0500 | Windows | High | ORG029 | Tech | 4 |
| S0372 | Windows | Medium | ORG117 | Finance | 4 |
| S0268 | Windows | Medium | ORG061 | Healthcare | 4 |
| S0231 | Windows | Medium | ORG058 | Healthcare | 4 |
| S0174 | Windows | High | ORG082 | Tech | 4 |
| S0031 | Linux | High | ORG099 | Healthcare | 4 |

**Decision:** Six systems are tied at 4 incidents each. All top-6 are Windows (5) or Linux (1). No Mac systems appear in the top tier.

### Query: Incidents by OS Type

```sql
SELECT
    s.os_type,
    COUNT(*) as incident_count,
    COUNT(DISTINCT s.system_id) as systems_affected,
    ROUND(COUNT(DISTINCT s.system_id) * 100.0 /
        (SELECT COUNT(*) FROM systems s2 WHERE s2.os_type = s.os_type), 1) as pct_affected
FROM incident_systems isys
JOIN systems s ON isys.system_id = s.system_id
GROUP BY s.os_type
ORDER BY incident_count DESC;
```

**Result:**

| OS Type | Incidents | Systems Hit | % of Fleet |
|---------|-----------|-------------|------------|
| Windows | 190 | 124 (58.2% of 213) |
| Mac | 156 | 116 (57.1% of 203) |
| Linux | 154 | 103 (56.0% of 184) |

### Query: Incidents by System Criticality

```sql
SELECT
    s.criticality,
    COUNT(*) as incident_count,
    COUNT(DISTINCT s.system_id) as systems_affected
FROM incident_systems isys
JOIN systems s ON isys.system_id = s.system_id
GROUP BY s.criticality
ORDER BY CASE s.criticality
    WHEN 'High' THEN 1 WHEN 'Medium' THEN 2 WHEN 'Low' THEN 3
END;
```

**Result:**

| Criticality | Incidents | Systems |
|-------------|-----------|---------|
| High | 200 | 128 |
| Medium | 173 | 120 |
| Low | 127 | 95 |

### Query: Critical-Severity Incidents on High-Criticality Systems

```sql
SELECT
    si.incident_id, si.incident_type, si.severity,
    s.system_id, s.os_type, s.criticality,
    o.industry, o.country
FROM incident_systems isys
JOIN security_incidents si ON isys.incident_id = si.incident_id
JOIN systems s ON isys.system_id = s.system_id
JOIN organizations o ON s.org_id = o.org_id
WHERE si.severity = 'Critical' AND s.criticality = 'High'
ORDER BY si.discovered_date DESC
LIMIT 15;
```

**Result:** 15 Critical incidents on High-criticality systems were found, spanning all three incident types and all industries. These represent the highest-priority combinations for remediation.

**Observations:**
- Windows leads in absolute incident count (190), but also has the most systems in the fleet (213). The affected-rate is similar across OS types (56-58%), so no single OS is dramatically more vulnerable than others.
- High-criticality systems have the most incidents (200), which is concerning but expected -- high-criticality systems are high-value targets and may receive more monitoring (detection bias).
- The top 6 most-incident-prone systems are overwhelmingly Windows (5 of 6). Windows systems account for all the 4-incident systems, which aligns with Windows being the most-attacked platform in general.
- Healthcare and Tech industries appear frequently among the most vulnerable systems, which tracks with real-world targeting patterns (healthcare for data value, tech for infrastructure access).

---

## Step 5: Network Events -- Anomalous Patterns

**What I did:** Analyzed `network_events` for distribution patterns, temporal trends, and cross-referenced with security incidents to find systems under compound threat.

### Query: Event Type Distribution

```sql
SELECT event_type, COUNT(*) as count,
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM network_events), 1) as pct
FROM network_events
GROUP BY event_type
ORDER BY count DESC;
```

**Result:**

| Event Type | Count | % |
|------------|-------|---|
| Network Scan | 1,303 | 26.1% |
| Malware Alert | 1,248 | 25.0% |
| Login | 1,235 | 24.7% |
| File Access | 1,214 | 24.3% |

### Query: Event Severity Distribution

```sql
SELECT severity, COUNT(*) as count,
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM network_events), 1) as pct
FROM network_events
GROUP BY severity
ORDER BY CASE severity
    WHEN 'Critical' THEN 1 WHEN 'High' THEN 2
    WHEN 'Medium' THEN 3 WHEN 'Low' THEN 4
END;
```

**Result:**

| Severity | Count | % |
|----------|-------|---|
| Critical | 1,278 | 25.6% |
| High | 1,278 | 25.6% |
| Medium | 1,216 | 24.3% |
| Low | 1,228 | 24.6% |

### Query: Temporal Pattern (Events per Month)

```sql
SELECT
    SUBSTR(timestamp, 1, 7) as month,
    COUNT(*) as total_events,
    SUM(CASE WHEN severity = 'Critical' THEN 1 ELSE 0 END) as critical,
    SUM(CASE WHEN severity = 'High' THEN 1 ELSE 0 END) as high
FROM network_events
GROUP BY month
ORDER BY month;
```

**Result:**

| Month | Total | Critical | High |
|-------|-------|----------|------|
| 2023-01 | 308 | 76 | 83 |
| 2023-02 | 262 | 69 | 67 |
| 2023-03 | 268 | 70 | 65 |
| 2023-04 | 305 | 82 | 76 |
| 2023-05 | 321 | 79 | 85 |
| 2023-06 | 297 | 71 | 72 |
| 2023-07 | 320 | 80 | 94 |
| 2023-08 | 326 | 83 | 80 |
| 2023-09 | 275 | 69 | 67 |
| 2023-10 | 304 | 74 | 86 |
| 2023-11 | 312 | 76 | 83 |
| 2023-12 | 317 | 88 | 73 |
| 2024-01 | 317 | 86 | 71 |
| 2024-02 | 307 | 72 | 79 |
| 2024-03 | 332 | 87 | 81 |
| 2024-04 | 282 | 70 | 77 |
| 2024-05 | 147 | 46 | 39 |

### Query: Systems with Both Network Events AND Security Incidents

```sql
SELECT
    s.system_id, s.os_type, s.criticality,
    ne_stats.network_events, ne_stats.critical_net_events,
    inc_stats.incidents,
    GROUP_CONCAT(DISTINCT si.incident_type) as incident_types
FROM systems s
JOIN (
    SELECT system_id, COUNT(*) as network_events,
           SUM(CASE WHEN severity = 'Critical' THEN 1 ELSE 0 END) as critical_net_events
    FROM network_events GROUP BY system_id
) ne_stats ON s.system_id = ne_stats.system_id
JOIN (
    SELECT system_id, COUNT(*) as incidents
    FROM incident_systems GROUP BY system_id
) inc_stats ON s.system_id = inc_stats.system_id
JOIN incident_systems isys ON s.system_id = isys.system_id
JOIN security_incidents si ON isys.incident_id = si.incident_id
GROUP BY s.system_id
ORDER BY ne_stats.critical_net_events DESC, inc_stats.incidents DESC
LIMIT 15;
```

**Result (top 5 compound-threat systems):**

| System | OS | Crit | Net Events | Critical Net | Incidents | Types |
|--------|------|------|------------|-------------|-----------|-------|
| S0186 | Windows | Low | 15 | 7 | 1 | Malware |
| S0452 | Windows | Medium | 15 | 7 | 1 | Data Breach |
| S0045 | Linux | Low | 12 | 6 | 1 | Unauthorized Access |
| S0206 | Windows | Low | 13 | 6 | 1 | Data Breach |
| S0261 | Mac | High | 13 | 5 | 3 | Data Breach, Unauthorized Access |

**Observations:**
- Event types and severities are nearly uniformly distributed (~25% each). This is a strong indicator of synthetically generated data -- real network events typically show heavy skew (Login events dominate, Low severity is most common).
- The temporal pattern shows a relatively steady event rate (~270-330/month) through 2023-2024, with a partial month in May 2024 (147 events). No obvious spike that would indicate a coordinated attack campaign.
- February 2023 and September 2023 show slight dips (~262-275 events), but these are not statistically significant given the range of variation.
- S0261 (Mac, High criticality) stands out as the most compound-threatened system: 3 incidents (Data Breach + Unauthorized Access) combined with 13 network events (5 critical). This system deserves priority investigation.
- S0186 and S0452 have the most critical network events (7 each) but only 1 incident each. These could be systems where attack attempts are being detected before escalating to full incidents -- or systems where incidents are being under-reported.
- Several of the most network-active systems are Low criticality. This is worth investigating: low-criticality systems might receive less monitoring, making them attractive pivot points.

---

## Summary of Findings

1. **Incident landscape:** Malware is the most common incident type (37%), with severity roughly evenly spread. The even distribution suggests synthetic data or comprehensive triage.

2. **Login security:** A 49.3% overall failure rate is anomalously high. Two users have 100% failure rates (U0279, U1491) and should be investigated for compromised or locked accounts. Failure patterns are uniform across roles.

3. **System vulnerability:** Windows systems lead in absolute incident counts (190) but affect similar proportions across all OS types (~57%). High-criticality systems are disproportionately targeted (200 incidents vs 127 for Low). The top 6 most-incident-prone systems are predominantly Windows.

4. **Network anomalies:** The most actionable finding is the compound-threat analysis -- systems like S0261 that show both high network event volumes and multiple security incidents. These represent convergence points where detection signals and actual incidents overlap, warranting priority investigation. No temporal spikes were found suggesting a coordinated campaign.

5. **Data quality note:** The near-uniform distributions across most categorical dimensions (event types, severities, OS incident rates, role-based failure rates) suggest this is synthetically generated data. In real security logs, these distributions are typically highly skewed.
