-- Supabase schema (optional)
create table if not exists topics (id bigserial primary key, niche text, keyword text, longtails jsonb default '[]', score numeric default 0, status text default 'new', created_at timestamptz default now());
create table if not exists assets (id bigserial primary key, type text, slug text unique, url text, status text default 'draft', revenue_to_date numeric default 0, created_at timestamptz default now());
create table if not exists jobs (id bigserial primary key, agent text, payload jsonb, result jsonb, created_at timestamptz default now());
create table if not exists sales (id bigserial primary key, source text, product_id text, amount numeric default 0, ts timestamptz default now());
create table if not exists api_usage (id bigserial primary key, api_id text, calls integer default 0, subscribers integer default 0, mrr numeric default 0, ts timestamptz default now());
create table if not exists ledger (id smallint primary key default 1, principal numeric default 100.00, profit_total numeric default 0.00, spending_unlocked jsonb default '{}'::jsonb, updated_at timestamptz default now());
insert into ledger (id) values (1) on conflict (id) do nothing;
