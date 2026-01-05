# Security policy

Jiraffe takes security seriously and encourages responsible disclosure of framework vulnerabilities.

## Supported versions

Jiraffe is actively developed on the latest release branch. Older versions may not receive security updates.

Users are encouraged to run the latest version.

## Reporting security issues

If you discover a security vulnerability **in Jiraffe itself** (not a Jira vulnerability), please report it responsibly.

### How to report

- **Do not** open a public GitHub issue
- Email the maintainer directly or use GitHub private advisories
- Include:
  - Jiraffe version
  - Proof of concept (if available)
  - Impact assessment
  - Reproduction steps

## Scope

This policy applies to:

- Jiraffe core framework
- Recon modules
- Exploit modules
- Supporting libraries bundled with Jiraffe

This policy does **not** apply to:

- Vulnerabilities in Atlassian Jira
- Misconfigurations detected by Jiraffe
- Third-party services assessed using Jiraffe

## Security philosophy

Jiraffe is designed with the following guarantees:

- Reconnaissance is performed before exploitation
- Exploitation is explicit and operator-controlled
- Compatibility checks reduce false positives
- Safe "check-only" modes are supported
- No automatic shells or persistence mechanisms exist

## Usage

Jiraffe is intended for:

- Authorized security testing
- Defensive research
- Internal assessments
- Bug bounty programs

Using Jiraffe against targets without permission is illegal.

The maintainer assumes **no liability** for misuse.

## Responsible disclosure

Jiraffe follows responsible disclosure principles and aims to improve the security posture of Jira deployments without encouraging abuse or indiscriminate exploitation.
