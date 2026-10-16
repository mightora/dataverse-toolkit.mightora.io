/* Public-beta Configuration Migration Studio behaviour tests — Node built-ins only. */
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');

const file = path.join(__dirname, '..', 'webresources', 'mgt_migration.html');
const html = fs.readFileSync(file, 'utf8');
const script = html.match(/<script>\s*(const app=[\s\S]*?)<\/script>/)?.[1];
assert.ok(script, 'Inline migration application script must exist');

function fakeNode() {
  return {
    textContent: '', value: '', hidden: false, checked: false, disabled: false,
    className: '', dataset: {}, files: [], scrollTop: 0, scrollHeight: 0,
    addEventListener() {}, replaceChildren() {}, appendChild() {}, remove() {},
    setAttribute() {}, getAttribute() { return null; }, classList: { add() {}, remove() {} }
  };
}
const nodes = new Map();
const document = {
  getElementById(id) {
    if (!nodes.has(id)) nodes.set(id, fakeNode());
    return nodes.get(id);
  },
  createElement(tag) { return Object.assign(fakeNode(), { tagName: tag }); },
  querySelectorAll() { return []; },
  body: fakeNode()
};
let networkCalls = 0;
const ctx = {
  document, window: { scrollTo() {} },
  location: { search: '?demo=1', protocol: 'https:', hostname: 'dataverse-tools.mightora.io' },
  URLSearchParams, URL, Blob,
  fetch() { networkCalls++; throw Error('Demo must never contact Dataverse'); },
  setTimeout() {},
  console
};
const app = vm.runInNewContext(script + '\napp;', ctx, { timeout: 3000 });
const valid = app.samplePackage();
assert.equal(valid.format, 'mightora-configuration-data');
assert.equal(app.parsePackage(valid), 2, 'Sample package contains two records');
assert.equal(app.validateSchema(valid.schema).tables.length, 1);

function cloned() { return JSON.parse(JSON.stringify(valid)); }
const invalidGuid = cloned();
invalidGuid.tables[0].rows[0].mgt_settingid = 'not-a-guid';
assert.throws(() => app.parsePackage(invalidGuid), /Invalid record GUID/);
const extraField = cloned();
extraField.tables[0].rows[0].unexpected = 'bad';
assert.throws(() => app.parsePackage(extraField), /Field not permitted/);
const dupe = cloned();
dupe.tables[0].rows[1].mgt_settingid = dupe.tables[0].rows[0].mgt_settingid;
assert.throws(() => app.parsePackage(dupe), /Duplicate record GUID/);
const wrongFormat = cloned();
wrongFormat.format = 'microsoft-configuration-migration-zip';
assert.throws(() => app.parsePackage(wrongFormat), /Invalid or unsupported package/);
assert.equal(networkCalls, 0, 'Demo mode must not issue network calls');
assert.ok(!html.includes('beacon.min.js'), 'No Cloudflare tracking inside Dataverse HTML');

console.log('Configuration Migration Studio: sample, schema, invalid GUID, unexpected field, duplicate, format and no-network assertions passed.');
