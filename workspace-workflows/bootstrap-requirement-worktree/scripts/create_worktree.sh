#!/usr/bin/env bash

set -euo pipefail

usage() {
  cat <<'EOF'
Usage: create_worktree.sh --repo PATH --path PATH --branch NAME [--remote NAME]

Fetch the remote and create a new branch/worktree from its latest default branch.
Existing branches and target paths are never reused or overwritten.
EOF
}

die() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

repo=""
target=""
branch=""
remote="origin"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo)
      [[ $# -ge 2 ]] || die "--repo requires a value"
      repo="$2"
      shift 2
      ;;
    --path)
      [[ $# -ge 2 ]] || die "--path requires a value"
      target="$2"
      shift 2
      ;;
    --branch)
      [[ $# -ge 2 ]] || die "--branch requires a value"
      branch="$2"
      shift 2
      ;;
    --remote)
      [[ $# -ge 2 ]] || die "--remote requires a value"
      remote="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      die "unknown argument: $1"
      ;;
  esac
done

[[ -n "$repo" ]] || die "--repo is required"
[[ -n "$target" ]] || die "--path is required"
[[ -n "$branch" ]] || die "--branch is required"

repo_root="$(git -C "$repo" rev-parse --show-toplevel 2>/dev/null)" || die "not a Git worktree: $repo"
repo_root="$(cd "$repo_root" && pwd -P)"
git -C "$repo_root" remote get-url "$remote" >/dev/null 2>&1 || die "remote does not exist: $remote"
git check-ref-format --branch "$branch" >/dev/null 2>&1 || die "invalid branch name: $branch"

[[ ! -e "$target" ]] || die "target path already exists: $target"
git -C "$repo_root" show-ref --verify --quiet "refs/heads/$branch" && die "branch already exists: $branch"

git -C "$repo_root" fetch "$remote" --prune

default_branch=""
remote_head="$(git -C "$repo_root" symbolic-ref --quiet --short "refs/remotes/$remote/HEAD" 2>/dev/null || true)"
if [[ "$remote_head" == "$remote/"* ]] && git -C "$repo_root" show-ref --verify --quiet "refs/remotes/$remote/${remote_head#"$remote/"}"; then
  default_branch="${remote_head#"$remote/"}"
fi

if [[ -z "$default_branch" ]]; then
  default_branch="$(git -C "$repo_root" ls-remote --symref "$remote" HEAD | awk '$1 == "ref:" && $3 == "HEAD" { sub("^refs/heads/", "", $2); print $2; exit }')"
  [[ -n "$default_branch" ]] || die "cannot determine default branch for remote: $remote"
  git -C "$repo_root" fetch "$remote" "+refs/heads/$default_branch:refs/remotes/$remote/$default_branch"
fi

base_ref="refs/remotes/$remote/$default_branch"
git -C "$repo_root" show-ref --verify --quiet "$base_ref" || die "remote default branch is unavailable: $remote/$default_branch"
git -C "$repo_root" show-ref --verify --quiet "refs/remotes/$remote/$branch" && die "remote branch already exists: $remote/$branch"

target_parent="$(dirname "$target")"
target_name="$(basename "$target")"
mkdir -p "$target_parent"
target_parent="$(cd "$target_parent" && pwd -P)"
target="$target_parent/$target_name"

git -C "$repo_root" worktree add -b "$branch" "$target" "$base_ref"

printf 'repository: %s\n' "$repo_root"
printf 'base: %s/%s\n' "$remote" "$default_branch"
printf 'branch: %s\n' "$branch"
printf 'worktree: %s\n' "$target"
