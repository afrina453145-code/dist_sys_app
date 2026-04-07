-- Run in Supabase SQL Editor or via CLI. Enables auth-linked profiles and live map positions.

create table if not exists public.profiles (
  id uuid primary key references auth.users (id) on delete cascade,
  role text not null default 'student' check (role in ('student', 'driver')),
  display_name text,
  updated_at timestamptz not null default now()
);

alter table public.profiles enable row level security;

create policy "profiles_select_own"
  on public.profiles for select
  using (auth.uid() = id);

create policy "profiles_update_own"
  on public.profiles for update
  using (auth.uid() = id);

create policy "profiles_insert_own"
  on public.profiles for insert
  with check (auth.uid() = id);

create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
begin
  insert into public.profiles (id, role)
  values (new.id, 'student')
  on conflict (id) do nothing;
  return new;
end;
$$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();

create table if not exists public.positions (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users (id) on delete cascade,
  role text not null check (role in ('student', 'driver')),
  lat double precision not null,
  lng double precision not null,
  updated_at timestamptz not null default now(),
  unique (user_id)
);

create index if not exists positions_role_updated_at_idx
  on public.positions (role, updated_at desc);

alter table public.positions enable row level security;

create policy "positions_select_authenticated"
  on public.positions for select
  to authenticated
  using (true);

create policy "positions_insert_own"
  on public.positions for insert
  to authenticated
  with check (auth.uid() = user_id);

create policy "positions_update_own"
  on public.positions for update
  to authenticated
  using (auth.uid() = user_id);

create policy "positions_delete_own"
  on public.positions for delete
  to authenticated
  using (auth.uid() = user_id);

alter publication supabase_realtime add table public.positions;
