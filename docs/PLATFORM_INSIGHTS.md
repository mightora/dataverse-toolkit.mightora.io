# Platform Insights — Public Beta

Install the updated unmanaged solution v1.0.0.4, or add `webresources/mgt_insights.html` as HTML web resource `mightora_mgt_insights` and add it to the model-driven app. The authenticated Dataverse user supplies the environment permissions. The website preview explicitly uses synthetic data (`?demo=1`).

## Environment scan

Read-only GET requests collect paged solutions, workflow definitions, app modules, canvas app metadata and users. Each source reports Loaded, Partial or Unavailable. Loaded means the request completed within the user's visibility; it does not prove unrestricted access. Scans stop at 20,000 records per source and mark remaining pages Partial. No table record contents, flow definitions, connection credentials or environment variable values are collected. Exported identifiers and names may still be sensitive.

Findings identify unmanaged solutions for policy review, quarantined inventory resources, missing returned owner metadata, and disabled Dataverse owners where those users were returned. Unmanaged does not imply incorrect deployment. Missing owner metadata does not prove orphaning. No usage inference is made from modification dates.

## Optional tenant inventory

1. Create or use an organisation-owned, single-tenant Entra application registration.
2. Add a **Single-page application** redirect URI matching the exact address displayed in connection setup. The address must be HTTPS and stable; use the installed web resource's direct URL rather than a model-driven app shell URL. Test tenant Conditional Access and popup behaviour.
3. Add the appropriate delegated query permission for **Power Platform API** (resource application ID `8578e004-a5c6-46e7-913e-12f58912df43`) following Microsoft's current API permission documentation. Obtain required admin consent. This tool requests the registration's configured `https://api.powerplatform.com/.default` scopes, so configure only necessary delegated permissions. Do not configure app-only access or client secrets for this tool.
4. Sign in with a supported inventory reader/admin, for example Global Reader or Power Platform Administrator. Environment security roles alone are insufficient for tenant inventory.
5. Enter tenant GUID and application client GUID, sign in, select Tenant and scan. Entra authorisation-code authentication uses S256 PKCE, same-origin popup/state validation and in-memory tokens. API endpoint: `POST https://api.powerplatform.com/resourcequery/resources/query?api-version=2024-10-01`; the POST performs a resource query, not a resource change.

Commercial cloud only. No proxy or unattended collector is provided. Microsoft OAuth, popup opener behaviour and inventory API CORS must work from the deployment origin. A denied request is reported, not silently replaced by sample data. These integration requirements have **not** been verified against a tenant. Clearing the local connection clears the token/results; it does not sign the user out of Microsoft globally.

## Reports and offline behaviour

JSON stores a sanitised snapshot plus scope, context, capture time and coverage. CSV exports the complete collected inventory with spreadsheet formula injection protection. Print provides a report that can be saved as PDF. Native editable DOCX/PPTX exports are not included in this release.

A previous JSON snapshot can be compared with the current scan only when scope, context, sample/live mode and collection coverage match. Removed visibility is labelled **No longer returned**, not deleted. Snapshots are user-exported files; no automatic browser persistence is used. Live scans need internet and sign-in. The downloaded HTML can show the synthetic preview offline; this is not an offline tenant scan.

Not collected: usage, flow runs/failures, historical audit, DLP policy evaluation, full effective permissions, licence compliance, tenant-wide disabled/deleted users or all CoE data. Connector metadata is preview and may omit built-in actions and some resource types. No AI service receives data.

## Validation before operational use

In a non-production environment, import v1.0.0.4, open Platform Insights from Diagnostics, and scan with both restricted and administrative users. Confirm pagination and coverage, exports, snapshot comparison, Microsoft sign-in and tenant inventory. Inspect DevTools Network for unexpected domains. Automated tests verify core logic and packaging, not successful installation or tenant access.

Microsoft references:
- https://learn.microsoft.com/en-us/power-platform/admin/inventory-api
- https://learn.microsoft.com/en-us/power-platform/admin/power-platform-inventory
- https://learn.microsoft.com/en-us/power-platform/admin/programmability-authentication-v2
