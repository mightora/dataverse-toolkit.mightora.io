# Model-driven app integration (v0.3 beta)

The repository includes a declarative list of all eleven intended model-driven app pages in [app-navigation.json](app-navigation.json).

The new page is **Configuration Migration Studio**:
- HTML source: `webresources/mgt_migration.html`
- Web resource logical name: `mgt_/migration.html`
- App: `mgt_DataverseToolkit`
- Section: **Data Management**
- Access: restricted to authorised migration administrators, because it can perform writes.

## Maker setup
1. Open a **development Dataverse environment** using Power Apps.
2. Ensure solution components for the existing ten tools are imported or already present.
3. Create HTML web resource `mgt_/migration.html` from the downloaded HTML in the **same unmanaged solution**.
4. Edit the model-driven app `mgt_DataverseToolkit`. Add a new web-resource page and select `mgt_/migration.html`. Name it **Configuration Migration Studio** under Data Management.
5. Publish and test with deliberately limited test data and a non-production account.
6. Make sure appropriate role-based app access and Dataverse privileges are applied; a hidden navigation item alone is **not** a security boundary.
7. Export the solution from Dataverse via standard ALM. Import it into a clean development environment before calling the solution a supported download.

**Status:** Source and navigation plan prepared, not yet installed into a connected Dataverse instance. A Microsoft-generated, successfully import-tested solution ZIP remains outstanding.

## Cross-environment usage
Run this same page in the source environment to export a Mightora JSON data package. Download it to a secure storage location. Then open the page in the target environment, upload the JSON, validate the target schema, enter the exact target hostname and complete the safety confirmations. Source and target must each host this HTML web resource.

No external token brokers, Azure Functions or cross-tenant authentication are required for this workflow; the browser uses the current model-driven app session in each environment.
