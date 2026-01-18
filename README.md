# Synapse_X_RAG
Prototype for a Local RAG based hybrid Vector-RDB AI Agent 

# 🔀 Git Workflow Guide (READ THIS BEFORE CODING)

This project uses a **module → develop → main** workflow.
Follow this exactly to avoid conflicts and broken code.

--------------------------------------------------

## 🌿 Branch Rules (IMPORTANT)

- ❌ Do NOT push directly to `main`
- ❌ Do NOT push directly to `develop`
- ✅ ALL work must be done on your own module branch
- ✅ ALL merges happen through Pull Requests (PRs)

Branches:
- `main` → stable / deployable
- `develop` → integration & testing
- `module-<your-name>` → your personal work branch

--------------------------------------------------

## 👤 YOUR DAILY WORKFLOW

### 1️⃣ Switch to your module branch
```bash
git checkout module-yourname
git pull origin module-yourname
```

---

### 2️⃣ Work on your module only

Make changes **only** related to your assigned module.

---

### 3️⃣ Commit your changes

Commit often with clear messages.

```bash
git add .
git commit -m "Add initial backend logic"
```

---

### 4️⃣ Push your branch

```bash
git push origin module-yourname
```

---

## 🔁 SUBMITTING YOUR WORK (PULL REQUEST)

When your module is ready (or partially ready):

1. Go to GitHub → Pull Requests → New Pull Request
2. Base branch: `develop`
3. Compare branch: `module-yourname`
4. Request at least **1 reviewer**
5. ❌ Do NOT merge your own PR unless approved

---

## 🧪 FIRST DRAFT INTEGRATION PHASE

After ALL modules are submitted:

* Module branches are merged into `develop`
* Conflicts are resolved in `develop`
* Bugs and integration issues are fixed in `develop`

All fixes follow this flow:

```text
develop → commit → push → PR → develop
```

---

## 🔄 AFTER INTEGRATION (GROUP WORK)

Everyone pulls the latest `develop`:

```bash
git checkout develop
git pull origin develop
```

From here:

* Small updates → commit directly to `develop`
* Large or risky changes → create a new branch

```bash
git checkout -b fix-something
```

Then PR back into `develop`.

---

## 🚀 FINAL RELEASE

When everything is tested and working:

1. Create PR: `develop` → `main`
2. Final review
3. Merge into `main`

`main` is the final deployable version.

---

## 📝 COMMIT MESSAGE FORMAT

Use short, clear messages:

```
Add login validation
Fix API error handling
Refactor database schema
```

---

## ❗ COMMON MISTAKES TO AVOID

* 🚫 Pushing to `main` or `develop`
* 🚫 Working on the wrong branch
* 🚫 Merging without review
* 🚫 Leaving conflicts unresolved

---

## 🆘 HELPFUL COMMANDS

```bash
git branch -a          # see all branches
git status             # check current state
git pull origin <branch>
git push origin <branch>
```

---

## ✅ SUMMARY

```text
module branch → PR → develop → test & fix → PR → main
```

If unsure — ASK BEFORE PUSHING.
