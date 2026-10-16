# Install in Power Apps

Create an unmanaged solution using your preferred publisher in a Dataverse development environment. Add each HTML file from webresources/ as an HTML web resource using the names: 

- `mgt_/trace.html`
- `mgt_/metadata.html`
- `mgt_/fetchxml.html`
- `mgt_/counter.html`
- `mgt_/solutions.html`
- `mgt_/relationships.html`

Create a model-driven app, add the ten web resources as pages, publish, and validate. Export a managed solution via Power Apps or the Power Platform CLI after environment testing.

The experimental combined solution created during prototyping was manually authored and has NOT been import-tested. Do not use in production without validation.


Additional Public Beta HTML web resources:
- `mgt_/webresources.html`
- `mgt_/views.html`
- `mgt_/security.html`
- `mgt_/environment.html`

## Add Configuration Migration Studio to the Model-Driven App

1. In your development environment, open the existing Mightora Dataverse Toolkit unmanaged solution.
2. Upload `webresources/mgt_migration.html` as an **HTML Web Resource** named `mgt_/migration.html`, using the `mgt` publisher prefix.
3. Open the model-driven app designer for `mgt_DataverseToolkit`, add a **Web resource page**, and select `mgt_/migration.html`. Give the page the title **Configuration Migration Studio** under a **Data Management** group.
4. Save, publish and validate with the test user roles. The UI uses existing Dataverse authentication; no client secret is required.
5. Include the web resource and app page in your Dataverse solution and export through Power Apps / Power Platform CLI after verification.

The GitHub Pages demo never writes. The combined imported app solution ZIP is not validated; this step is a maker-environment integration instruction, not a claim of an already-published app update.
