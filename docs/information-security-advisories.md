---
description: Information on relevant CVEs and security issues for clients
---

# Information Security Advisories

## December 2022

### [CVE-2022-42475](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-42475)

<table data-header-hidden><thead><tr><th>December 22-001</th><th data-hidden></th></tr></thead><tbody><tr><td><strong>Description:</strong> A heap-based buffer overflow vulnerability [<a href="https://cwe.mitre.org/data/definitions/122.html">CWE-122</a>] in FortiOS SSL-VPN may allow a remote unauthenticated attacker to execute arbitrary code or commands via specifically crafted requests.</td><td></td></tr><tr><td><strong>Severity:</strong> 9.3</td><td></td></tr><tr><td><strong>Impact to CoreWeave Platform:</strong> Currently no known impact to CoreWeave Platform</td><td></td></tr><tr><td><strong>Potentially Affected Clients:</strong> Clients using FortiOS</td><td></td></tr><tr><td><strong>Recommended Actions:</strong> <a href="https://www.fortiguard.com/psirt/FG-IR-22-398">Vendor-recommended mitigations</a></td><td></td></tr></tbody></table>

[FortiGuard Labs](https://www.fortiguard.com/psirt/FG-IR-22-398) has confirmed at least one instance of vulnerability [**CVE-2022-42475**](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-42475) being exploited in the wild. Given the high value (CVE critical severity rating **9.3**) and relatively low complexity of this vulnerability, CoreWeave strongly recommends upgrading to an unaffected version of FortiOS on an accelerated patch schedule, according to [vendor recommendations](https://www.fortiguard.com/psirt/FG-IR-22-398).\
\
Vulnerability checks for **CVE-2022-42475** are available from a variety of sources. Please use caution when running any script or application to ensure it is safe.

**At this time there is no impact to CoreWeave's platform**, however customers who have FortiOS running within their environment are advised to review the [vendor-recommended mitigations](https://www.fortiguard.com/psirt/FG-IR-22-398), and take appropriate self measures to upgrade their deployments and evaluate their systems for any indicators of compromise. Our cyber security team is closely monitoring the situation, and will provide important updates should more information become available.
