#!/usr/bin/env bash

set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
subject="$script_dir/create_worktree.sh"
test_root="$(mktemp -d "${TMPDIR:-/tmp}/bootstrap-worktree-test.XXXXXX")"

cleanup() {
  rm -rf -- "$test_root"
}
trap cleanup EXIT

fail() {
  printf 'FAIL: %s\n' "$*" >&2
  exit 1
}

assert_eq() {
  local expected="$1"
  local actual="$2"
  local message="$3"
  [[ "$expected" == "$actual" ]] || fail "$message (expected=$expected actual=$actual)"
}

create_fixture() {
  local name="$1"
  local fixture="$test_root/$name"
  local origin="$fixture/origin.git"
  local seed="$fixture/seed"
  local repo="$fixture/repo"

  mkdir -p "$fixture"
  git init --bare --initial-branch=main "$origin" >/dev/null
  git init --initial-branch=main "$seed" >/dev/null
  git -C "$seed" config user.name "Skill Test"
  git -C "$seed" config user.email "skill-test@example.com"
  printf 'initial\n' >"$seed/state.txt"
  git -C "$seed" add state.txt
  git -C "$seed" commit -m initial >/dev/null
  git -C "$seed" remote add origin "$origin"
  git -C "$seed" push -u origin main >/dev/null
  git clone "$origin" "$repo" >/dev/null 2>&1

  printf '%s\n' "$fixture"
}

test_uses_latest_remote_default_branch() {
  local fixture
  fixture="$(create_fixture latest)"
  local seed="$fixture/seed"
  local repo="$fixture/repo"
  local target="$fixture/worktrees/requirement/repo"

  printf 'remote-latest\n' >"$seed/state.txt"
  git -C "$seed" add state.txt
  git -C "$seed" commit -m remote-latest >/dev/null
  git -C "$seed" push origin main >/dev/null
  local expected_head
  expected_head="$(git -C "$seed" rev-parse HEAD)"

  printf 'user change\n' >"$repo/local-only.txt"
  "$subject" --repo "$repo" --path "$target" --branch feat/requirement >/dev/null

  assert_eq "$expected_head" "$(git -C "$target" rev-parse HEAD)" "worktree must start at latest remote default branch"
  assert_eq "feat/requirement" "$(git -C "$target" branch --show-current)" "worktree must use requested branch"
  [[ -f "$repo/local-only.txt" ]] || fail "source checkout changes must be preserved"
}

test_discovers_default_branch_without_remote_head_ref() {
  local fixture
  fixture="$(create_fixture fallback)"
  local repo="$fixture/repo"
  local target="$fixture/worktrees/requirement/repo"

  git -C "$repo" symbolic-ref -d refs/remotes/origin/HEAD
  "$subject" --repo "$repo" --path "$target" --branch feat/fallback >/dev/null

  assert_eq "feat/fallback" "$(git -C "$target" branch --show-current)" "fallback path must create the requested branch"
  assert_eq "$(git -C "$repo" rev-parse origin/main)" "$(git -C "$target" rev-parse HEAD)" "fallback must resolve the remote default branch"
}

test_refuses_existing_branch() {
  local fixture
  fixture="$(create_fixture collision)"
  local repo="$fixture/repo"
  local target="$fixture/worktrees/requirement/repo"

  git -C "$repo" branch feat/existing
  if "$subject" --repo "$repo" --path "$target" --branch feat/existing >"$fixture/stdout" 2>"$fixture/stderr"; then
    fail "existing branch must be rejected"
  fi
  [[ ! -e "$target" ]] || fail "rejected branch must not create a worktree"
  grep -q "already exists" "$fixture/stderr" || fail "collision error must explain the existing branch"
}

test_uses_latest_remote_default_branch
test_discovers_default_branch_without_remote_head_ref
test_refuses_existing_branch

printf 'PASS: create_worktree.sh\n'
