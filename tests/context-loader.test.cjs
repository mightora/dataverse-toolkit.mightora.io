// Regression: Microsoft ClientGlobalContext.js.aspx must resolve for flat,
// nested/publisher-virtual-folder and versioned Dataverse web resource URLs.
// This is a URL-path test, NOT a live authentication or tenant integration test.
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const assert=require('node:assert/strict');

const project=path.resolve(__dirname,'..');
const slugs=['trace','metadata','fetchxml','counter','solutions','relationships',
             'webresources','views','security','environment','migration'];
for(const slug of slugs){
 const file=path.join(project,'webresources','mgt_'+slug+'.html');
 const html=fs.readFileSync(file,'utf8');
 const loader=html.match(/<script>([\s\S]*?)<\/script>/i)?.[1];
 assert.ok(loader && loader.includes('ClientGlobalContext.js.aspx'),file);
 function resolve(pathname,search='',protocol='https:'){
  let output='';
  const location={pathname,protocol,search};
  vm.runInNewContext(loader,{
    location,URLSearchParams,decodeURIComponent,
    document:{write(v){output+=v}},
  },{timeout:2000});
  return output;
 }
 for(const pair of [
   ['/WebResources/mgt_'+slug+'.html','ClientGlobalContext.js.aspx'],
   ['/WebResources/mgt_/'+slug+'.html','../ClientGlobalContext.js.aspx'],
   ['/%7B2026%7D/WebResources/mgt_'+slug+'.html','ClientGlobalContext.js.aspx'],
   ['/%7B2026%7D/WebResources/mgt_/nested/'+slug+'.html','../../ClientGlobalContext.js.aspx']
 ]){
  assert.ok(resolve(pair[0]).includes('src="'+pair[1]+'"'),
    slug+': context path incorrect for '+pair[0]);
 }
 assert.equal(resolve('/WebResources/mgt_'+slug+'.html','?demo=1'),'');
 assert.equal(resolve('/WebResources/mgt_'+slug+'.html','','file:'),'');
}
console.log('11 maintained context loaders correctly resolve flat, nested and versioned paths.');
