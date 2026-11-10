const postgres = require('C:/Users/mateu/AppData/Local/npm-cache/_npx/43414d9b790239bb/node_modules/postgres');

async function main() {
  const sql = postgres('postgres://paperclip:paperclip@127.0.0.1:54329/paperclip');
  
  const [agent] = await sql`SELECT id, name, metadata, adapter_config FROM agents WHERE id = 'a9850b87-19a5-49ae-9098-fd5d71dc4195'`;
  console.log('AGENT:', JSON.stringify(agent, null, 2));

  const docs = await sql`SELECT * FROM documents`;
  console.log('DOCS:', docs);

  await sql.end();
}

main().catch(console.error);
