# Git Workflow Conventions

## 1. Purpose

Follow this workflow for every project phase to maintain a clean Git history, reviewable changes, and consistent phase completion.

Never work directly on `main`.

## 2. Branch Naming

Create a dedicated feature branch for each phase.

**Convention:**

`feature/<phase-name>`

**Examples:**

- `feature/requirements`
- `feature/database-design`
- `feature/backend-setup`
- `feature/database-setup`
- `feature/backend-models`

Create the branch from an up-to-date `main` branch.

```bash
git checkout main
git pull origin main
git checkout -b feature/<phase-name>
```

## 3. Review Changes Before Committing

Before staging changes:

```bash
git status
git diff
git diff --check
```

Verify that:

- Changes belong to the current phase.
- No unrelated files are included.
- No secrets, `.env` files, or generated files are accidentally staged.

Stage intended files explicitly when practical.

```bash
git add <file-paths>
```

Review staged changes:

```bash
git diff --cached
git diff --cached --check
```

## 4. Commit Message Convention

Use Conventional Commits.

**Format:**

`<type>: <imperative description>`

Common types:

| Type | Purpose |
| --- | --- |
| `feat:` | New functionality or implementation milestone |
| `fix:` | Bug fix |
| `test:` | Tests |
| `docs:` | Documentation |
| `refactor:` | Code restructuring without intended behavior changes |
| `chore:` | Configuration or maintenance |

Examples:

```text
feat: add SCMS database models
fix: correct enrollment validation
test: add course model tests
docs: document database design
chore: configure backend tooling
```

Commit conventions:

- Keep messages concise and specific.
- Describe the actual change.
- Avoid vague messages such as `changes`, `update`, `final`, or `test`.
- Keep commits focused on the current phase.

Commit the reviewed changes:

```bash
git commit -m "<type>: <description>"
```

## 5. Push the Feature Branch

Push the phase branch to GitHub:

```bash
git push -u origin feature/<phase-name>
```

Do not push phase implementation changes directly to `main`.

## 6. Pull Request Conventions

Create a Pull Request on GitHub.

**Base branch:** `main`  
**Compare branch:** `feature/<phase-name>`

Before submitting the PR, prepare these four separate, copyable artifacts:

1. PR title
2. PR description
3. Submit review comment
4. Extended description for merge

All four artifacts must be provided before PR submission.

### 6.1 PR Title

Use a concise title that identifies the change.

Examples:

```text
feat: add SCMS database models
chore: set up backend application
docs: define SCMS requirements
```

The title should reflect the actual implementation and use an appropriate Conventional Commit type.

### 6.2 PR Description

The PR description must contain these sections in this order:

```markdown
## Summary

## Implementation Details

## Verification

## Related Phase
```

Requirements:

- **Summary:** State the purpose of the change.
- **Implementation Details:** List the principal changes.
- **Verification:** Record checks actually performed and their results.
- **Related Phase:** Identify the project phase and its name.

Keep the description concise, specific, and focused on the current phase.

Do not claim that tests, builds, or checks passed unless they were actually run.

### 6.3 Submit Review Comment

Provide the review comment as a separate, copyable artifact.

Format:

```text
Reviewed and verified <feature or phase>:

- <Verified implementation detail>
- <Verified implementation detail>
- <Verification result>
- <Relevant scope boundary, if applicable>

**Approved**
```

Requirements:

- Start with a short introductory sentence.
- Use individual bullet points for verified results.
- Include only checks that were actually performed.
- Mention important scope boundaries where relevant.
- End with a clear outcome, such as `Approved for merge.`
- Do not include branch cleanup instructions.
- Do not claim that the live database schema was verified when only ORM metadata was inspected.

### 6.4 Extended Description for Merge

Provide the extended merge description as a separate, copyable artifact.

Format:

```text
<Short implementation summary>

- <Implementation deliverable>
- <Implementation deliverable>
- <Constraint, relationship, or configuration detail>
- <Verification result>
- Completed Phase <N> — <Phase Name>.
```

Requirements:

- Begin with a concise implementation summary.
- List the principal implementation changes as individual bullet points.
- Include relevant verification results.
- Mention important scope boundaries when applicable.
- The final point must use the format:

  `Completed Phase <N> — <Phase Name>.`

- Do not include after-merge commands or branch-cleanup instructions.
- Do not state that the Git workflow is pending.
- Do not claim that the phase is fully complete before the required workflow finishes.
- Use the prepared extended description as the merge commit message or description when creating the regular merge commit. Format it as individual bullet points where supported.
- Do not use the extended description as a squash commit message because **Squash and merge is not permitted** in this workflow.

The final completion statement describes the implementation milestone being merged. Actual phase completion must still be confirmed after the PR is merged and the post-merge workflow is finished.

## 7. Review and Merge

Before merging:

1. Review the PR diff and changed files.
2. Confirm that the changes belong to the intended phase.
3. Verify the implementation and checks described in the PR.
4. Submit the prepared review comment as a PR comment or review, as appropriate.
5. Resolve identified issues before merging.
6. **Always select Create a merge commit. Never use Squash and merge or Rebase and merge.**
7. Preserve the feature branch's individual commits in the resulting history on `main`.
8. Use the prepared extended description as the merge commit message or description, formatted as individual bullet points where supported.

Do not merge a PR that still has unresolved issues.

### Merge strategy

Use a regular merge commit to preserve individual feature-branch commits and explicitly record the integration of each phase into `main`.

This is the mandatory merge strategy for all project phases.

## 8. Post-Merge Workflow

After GitHub confirms that the PR has been merged, synchronize local `main`:

```bash
git checkout main
git pull origin main
```

Verify the latest commit and merged files:

```bash
git log -1 --oneline
git show --stat --oneline HEAD
git status
```

Delete the local feature branch:

```bash
git branch -d feature/<phase-name>
```

If the remote branch still exists, delete it:

```bash
git push origin --delete feature/<phase-name>
```

Confirm the current branch and working-tree state:

```bash
git branch --show-current
git status
```

Expected result:

- Current branch is `main`.
- Local `main` is synchronized with `origin/main`.
- The working tree is clean.
- The local feature branch is deleted.
- The remote feature branch is deleted, unless GitHub has already deleted it.

## 9. Phase Completion Criteria

A phase can be marked complete only when:

- [ ] Implementation matches the approved phase scope.
- [ ] Required verification has been performed.
- [ ] Changes have been reviewed and committed.
- [ ] Feature branch has been pushed.
- [ ] PR has been created with all required artifacts.
- [ ] PR review is complete and issues are resolved.
- [ ] PR has been merged into `main`.
- [ ] Local `main` has been synchronized with `origin/main`.
- [ ] Local and remote feature branches have been deleted.
- [ ] Working tree is clean.

Do not mark a phase complete merely because the implementation or commit is finished.

## 10. Mandatory Assistant Output for Every Phase

Before PR submission, always provide four separate, copyable artifacts:

1. **PR title**
2. **PR description** with `Summary`, `Implementation Details`, `Verification`, and `Related Phase`
3. **Submit review comment**, formatted pointwise
4. **Extended description for merge**, formatted pointwise and ending with `Completed Phase <N> — <Phase Name>.`

After providing these artifacts, explain the GitHub PR steps and post-merge commands separately.

### Merge strategy requirement

- Always use **Create a merge commit** when merging a pull request.
- Never use **Squash and merge** or **Rebase and merge**.
- Preserve the feature branch's individual commits in the resulting history on `main`.
- Use the prepared extended description as the merge commit message or description, formatted as individual bullet points where supported.

Keep the workflow consistent across phases. Adapt the content to the actual implementation, but do not omit required artifacts or completion checks.
