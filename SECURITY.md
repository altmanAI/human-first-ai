# Security Policy

`human-first-ai` is maintained by **AltmanAI**, a project of **Altman Family
Group LLC**. We treat security as a prerequisite for trust, not an
afterthought — the same philosophy behind the project's transparency-log and
values-gating design.

## Supported Versions

This project is in early, active development (pre-1.0). Until a `1.0`
release, only the `main` branch / latest tagged release receives security
fixes.

| Version | Supported |
|---|---|
| `main` / latest tag | ✅ |
| Older tags | ❌ |

Once the project reaches `1.0`, this table will be updated with a formal
support window for prior minor versions.

## Reporting a Vulnerability

**Please do not open a public GitHub issue for security vulnerabilities.**

Instead, report privately using one of these channels:

1. **Preferred:** GitHub's [private vulnerability reporting](https://github.com/altmanAI/human-first-ai/security/advisories/new) (Security tab → "Report a vulnerability").
2. **Email:** security@altmanai.dev (or the founder's contact on file if that
   address is not yet live — see the repository owner's GitHub profile).

When reporting, please include:
- A description of the vulnerability and its potential impact.
- Steps to reproduce (proof-of-concept code, if available).
- The affected version/commit.
- Your suggested severity, if you have one.

### What to expect

- **Acknowledgment:** within 5 business days.
- **Triage & severity assessment:** within 10 business days of acknowledgment.
- **Fix or mitigation plan:** communicated once triage is complete, with a
  timeline appropriate to severity (critical issues are prioritized
  immediately).
- **Credit:** with your permission, we will credit you in the release notes
  / changelog once a fix ships. We do not publicly disclose the report
  until a fix is available, unless you and we agree otherwise.

We ask reporters to give us a reasonable window to address an issue before
any public disclosure — standard coordinated disclosure practice.

## Credential & Secret Handling

- This repository must never contain real API keys, private keys, tokens,
  passwords, or customer data — in code, tests, fixtures, or commit history.
- Any example credentials in docs/tests are clearly fake placeholders (e.g.
  `sk-example-not-real`) and must be obviously non-functional.
- If a real secret is ever accidentally committed, treat it as compromised
  immediately: rotate/revoke it at the source, then scrub history. Do not
  rely on a force-push alone — assume anything pushed to a public remote
  may already be cached/scraped.
- Dependency and CI secrets (e.g. PyPI publish tokens) are managed via
  GitHub Actions encrypted secrets, scoped to the minimum required
  permissions, never printed to logs.

## Our Security Posture

- Dependencies are monitored via Dependabot (`.github/dependabot.yml`) for
  known vulnerabilities and kept current on a conservative, reviewed
  schedule — not auto-merged blindly.
- CI runs the full test suite on every push and pull request to `main`.
- We aim for branch protection on `main` (required reviews, required status
  checks, no force-push) — see the repository's branch protection settings
  for current status.
- This is a human-first project in more than name: security reports are
  read and answered by a human, not routed to a black hole.

Thank you for helping keep AltmanAI's open-source work trustworthy.
