# Install in Power Apps

Create an unmanaged solution using your preferred publisher in a Dataverse development environment. Add each HTML file from webresources/ as an HTML web resource using the names: 

- `mgt_/trace.html`
- `mgt_/metadata.html`
- `mgt_/fetchxml.html`
- `mgt_/counter.html`
- `mgt_/solutions.html`
- `mgt_/relationships.html`

Create a model-driven app, add the six web resources as pages, publish, and validate. Export a managed solution via Power Apps or the Power Platform CLI after environment testing.

The experimental combined solution created during prototyping was manually authored and has NOT been import-tested. Do not use in production without validation.
