const postgres = require('C:/Users/mateu/AppData/Local/npm-cache/_npx/43414d9b790239bb/node_modules/postgres');
const fs = require('fs');
const path = require('path');
const { randomUUID } = require('crypto');

async function main() {
  const sql = postgres('postgres://paperclip:paperclip@127.0.0.1:54329/paperclip');
  
  const projectCols = await sql`
    SELECT column_name, data_type, is_nullable 
    FROM information_schema.columns 
    WHERE table_name = 'projects'
  `;
  console.log('PROJECT COLS:', projectCols.map(c => `${c.column_name}: ${c.data_type} (null=${c.is_nullable})`));

  const agentCols = await sql`
    SELECT column_name, data_type, is_nullable 
    FROM information_schema.columns 
    WHERE table_name = 'agents'
  `;
  console.log('AGENT COLS:', agentCols.map(c => `${c.column_name}: ${c.data_type} (null=${c.is_nullable})`));

  await sql.end();
}

main().catch(console.error);
