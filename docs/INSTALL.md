# Mightora Dataverse Tools v1.0.0.3 — Unmanaged development installation

**Release:** Public Beta. The ZIP is a genuine Microsoft PAC-packed
unmanaged Dataverse solution, not the older web-resource distribution ZIP.

**Download:** https://github.com/mightora/dataverse-toolkit.mightora.io/raw/refs/heads/main/deployment/MightoraDataverseTools_1_0_0_3_unmanaged.zip

## Install into a development environment

1. Confirm you have a disposable development environment with a Dataverse database,
   appropriate admin or maker permissions, and a recent environment backup.
2. Go to https://make.powerapps.com, choose the development environment,
   then select **Solutions → Import solution**.
3. Choose `MightoraDataverseTools_1_0_0_3_unmanaged.zip`, not
   `mightora-dataverse-tools.zip` (the older HTML bundle).
4. Complete import and **Publish all customizations**.
5. Open **Apps → Mightora Dataverse Tools** and check the five navigation groups.
6. Verify the client connection first using **Environment Diagnostics**.
7. Test **Metadata Explorer**, **Record Counter**, **FetchXML Studio** and
   **FetchFlow** with tables the current user is authorised to read.
8. Check **Plugin Trace Explorer**, **Relationship Visualiser**, **Security
   Role Catalogue**, **View Query Inspector**, **Web Resource Browser** and
   both solution tools as users with different security roles.
9. Test REST and Configuration Migration **only with deliberately disposable
   data**. Both can invoke Dataverse plug-ins, business rules or flows.
10. Record failures with DevTools console and Network screenshots, including
    whether `ClientGlobalContext.js.aspx` returned 200 and the status of
    `/api/data/v9.2/WhoAmI()`. Remove customer IDs and record content
    before reporting issues publicly.

## Included navigation groups

| Group | Tools |
|---|---|
| Diagnostics | Plugin Trace Explorer, Record Counter, Environment Diagnostics |
| Tables and data model | Metadata Explorer, Relationship Visualiser, View Query Inspector, Web Resource Browser |
| Queries and APIs | FetchXML Studio, FetchFlow, REST Studio |
| Solutions and migration | Solution Inspector, Solution Explorer, Configuration Migration Studio |
| Security | Security Role Catalogue |

## Connection model

The original ten tools and Configuration Migration Studio load Microsoft's
`ClientGlobalContext.js.aspx` at the correct relative path for their actual
web-resource names, then perform same-origin Dataverse Web API calls using
the signed-in session. FetchFlow and REST Studio now use the same principle.
Solution Explorer uses a same-origin Dataverse-hosted page check and
authenticated API calls.

**No access tokens, secrets or external proxy are included** in the
solution. Dataverse privileges, CSP, tenant policies and app access still
control all operations. GitHub Pages previews use explicit sample mode;
sample records must not replace a missing live connection inside the app.

## Testing status and remaining limitations

The generated package passed static structure and Microsoft PAC packaging
checks. **A real Dataverse import and end-to-end API run have not yet been
performed in this conversation** and therefore production readiness cannot
be asserted.

The beta tools retain documented functional limits: record/page caps,
restricted metadata access, security role catalogue without privilege
resolution, only system views in View Query Inspector, and Mightora-only
JSON (not Microsoft-native ZIP/XML) in Configuration Migration Studio.

Keep the original v1.0.0.2 export for rollback/reference. See
[Dataverse connection troubleshooting](DATAVERSE_CONNECTIONS.md),
[configuration migration limitations](CONFIGURATION_MIGRATION.md) and
[full unpacked source](../deployment/mightora-dataverse-tools).
