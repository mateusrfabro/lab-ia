const postgres = require('C:/Users/mateu/AppData/Local/npm-cache/_npx/43414d9b790239bb/node_modules/postgres');
const { randomUUID } = require('crypto');

const COMPANY_ID = '0408b670-10fe-4746-9cea-6606fa5770ac'; // MonetPoint
const TECH_LEAD_ID = 'a9850b87-19a5-49ae-9098-fd5d71dc4195';
const DEFAULT_ENV_ID = '9bb094d5-8acc-4a6d-929b-587994d002b9';

async function main() {
  const sql = postgres('postgres://paperclip:paperclip@127.0.0.1:54329/paperclip');

  console.log('=== POVOANDO MONETPOINT NO PAPERCLIP ===\n');

  // 1. INSERIR PROJETOS
  const projects = [
    {
      id: randomUUID(),
      company_id: COMPANY_ID,
      name: 'MultiBet',
      description: 'Plataforma de inteligência e arbitragem de apostas esportivas / vertical iGaming',
      status: 'in_progress',
      lead_agent_id: TECH_LEAD_ID,
      color: '#10b981',
      icon: 'flame',
      visibility: 'open',
      execution_workspace_policy: {
        enabled: true,
        defaultMode: 'shared_workspace',
        sharedWorkspaceConcurrency: 'auto',
        workspaceDir: 'C:\\Users\\mateu\\OneDrive - PGX\\Projetos - Super Nova\\MultiBet'
      }
    },
    {
      id: randomUUID(),
      company_id: COMPANY_ID,
      name: 'Casa Livre',
      description: 'Programa Privado de Aquisição Imobiliária Planejada & Criativos 2D Motion (ConSociety Group)',
      status: 'in_progress',
      lead_agent_id: TECH_LEAD_ID,
      color: '#0842e6',
      icon: 'rocket',
      visibility: 'open',
      execution_workspace_policy: {
        enabled: true,
        defaultMode: 'shared_workspace',
        sharedWorkspaceConcurrency: 'auto',
        workspaceDir: 'C:\\Users\\mateu\\Downloads\\Projeto Dudu'
      }
    },
    {
      id: randomUUID(),
      company_id: COMPANY_ID,
      name: 'Lab IA & Comparador de Cartões',
      description: 'Laboratório de IA, funis de quiz paginados, esteira de cartões de crédito e cloakers',
      status: 'in_progress',
      lead_agent_id: TECH_LEAD_ID,
      color: '#8b5cf6',
      icon: 'code',
      visibility: 'open',
      execution_workspace_policy: {
        enabled: true,
        defaultMode: 'shared_workspace',
        sharedWorkspaceConcurrency: 'auto',
        workspaceDir: 'C:\\Users\\mateu\\Projects\\lab-ia'
      }
    }
  ];

  for (const p of projects) {
    const existing = await sql`SELECT id FROM projects WHERE company_id = ${COMPANY_ID} AND name = ${p.name}`;
    if (existing.length === 0) {
      await sql`
        INSERT INTO projects (
          id, company_id, name, description, status, lead_agent_id, 
          color, icon, visibility, execution_workspace_policy, 
          created_at, updated_at
        ) VALUES (
          ${p.id}, ${p.company_id}, ${p.name}, ${p.description}, ${p.status}, ${p.lead_agent_id},
          ${p.color}, ${p.icon}, ${p.visibility}, ${sql.json(p.execution_workspace_policy)},
          NOW(), NOW()
        )
      `;
      console.log(`[PROJETO CRIADO] ✓ ${p.name}`);
    } else {
      console.log(`[PROJETO JÁ EXISTE] • ${p.name}`);
    }
  }

  // 2. INSERIR SQUAD DE AGENTES
  const squad = [
    {
      name: 'Copywriter',
      role: 'marketing',
      title: 'Especialista em Copy de Vendas & VSL',
      capabilities: 'Copy de vendas persuasiva e honesta em PT-BR (PAS, AIDA, 4Ps), páginas de vendas, VSL, anúncios e e-mails.',
      instructionsFilePath: 'C:\\Users\\mateu\\.claude\\agents\\copywriter.md',
      paletteId: 'sunset'
    },
    {
      name: 'Code Quality',
      role: 'engineering',
      title: 'Auditor de Qualidade & Engenharia',
      capabilities: 'Auditoria de qualidade TypeScript/React/Next.js/Python, bugs reais, tipagem e estabilidade.',
      instructionsFilePath: 'C:\\Users\\mateu\\.claude\\agents\\code-quality.md',
      paletteId: 'cyber-neon'
    },
    {
      name: 'Growth Analytics',
      role: 'analytics',
      title: 'Analista de Growth & Funis',
      capabilities: 'Métricas do funil (conversão por etapa, CAC, LTV, ROAS, churn), instrumentação de pixels e tracking.',
      instructionsFilePath: 'C:\\Users\\mateu\\.claude\\agents\\growth-analytics.md',
      paletteId: 'ocean-breeze'
    },
    {
      name: 'Tráfego Pago',
      role: 'marketing',
      title: 'Gestor de Tráfego Meta & Google',
      capabilities: 'Estrutura de campanhas, segmentação, criativos/ângulos de anúncio, orçamento e métricas de tráfego pago.',
      instructionsFilePath: 'C:\\Users\\mateu\\.claude\\agents\\trafego-pago.md',
      paletteId: 'electric-grove'
    },
    {
      name: 'Ops Contingência',
      role: 'operations',
      title: 'Controle de Contingência & Isolamento',
      capabilities: 'MoreLogin, contas de anúncio, proxies, esteiras de contingência, pixels e isolamento de domínios.',
      instructionsFilePath: 'C:\\Users\\mateu\\.claude\\agents\\ops-contingencia.md',
      paletteId: 'muted-dream'
    }
  ];

  for (const a of squad) {
    const existing = await sql`SELECT id FROM agents WHERE company_id = ${COMPANY_ID} AND name = ${a.name}`;
    if (existing.length === 0) {
      const agentId = randomUUID();
      const adapterConfig = {
        graceSec: 15,
        timeoutSec: 0,
        maxTurnsPerRun: 1000,
        dangerouslySkipPermissions: true,
        instructionsFilePath: a.instructionsFilePath
      };
      const runtimeConfig = {
        heartbeat: {
          enabled: false,
          cooldownSec: 10,
          intervalSec: 300,
          wakeOnDemand: true,
          maxConcurrentRuns: 20,
          skipTimerWhenNoActionableWork: true
        }
      };
      const permissions = {
        canCreateAgents: true,
        canCreateSkills: true
      };
      const appearance = {
        schemaVersion: 1,
        characterVersion: 'cap-v1',
        paletteId: a.paletteId
      };

      await sql`
        INSERT INTO agents (
          id, company_id, name, role, title, status, reports_to, 
          capabilities, adapter_type, adapter_config, runtime_config,
          permissions, default_environment_id, appearance,
          lifecycle_state, lifecycle_holds, lifecycle_version,
          budget_monthly_cents, spent_monthly_cents, created_by_user_id,
          created_at, updated_at
        ) VALUES (
          ${agentId}, ${COMPANY_ID}, ${a.name}, ${a.role}, ${a.title}, 'idle', ${TECH_LEAD_ID},
          ${a.capabilities}, 'claude_local', ${sql.json(adapterConfig)}, ${sql.json(runtimeConfig)},
          ${sql.json(permissions)}, ${DEFAULT_ENV_ID}, ${sql.json(appearance)},
          'ready', '[]'::jsonb, 1,
          0, 0, 'local-board',
          NOW(), NOW()
        )
      `;
      console.log(`[AGENTE ADICIONADO] ✓ ${a.name} (${a.title}) -> Reporta para Tech Lead`);
    } else {
      console.log(`[AGENTE JÁ EXISTE] • ${a.name}`);
    }
  }

  console.log('\n=== MONETPOINT ATUALIZADO COM SUCESSO! ===');
  await sql.end();
}

main().catch(console.error);
