# Basic Commands  
- `git init` – Initialise a new repository  
- `git clone <repo_url>` – Clone an existing repository  
- `git add .` – Stage all changes  
- `git commit -m "Commit message"` – Commit staged changes  

# Branching & Merging  
- `git branch` – List all branches  
- `git checkout -b <branch_name>` – Create and switch to a new branch  
- `git merge <branch_name>` – Merge a branch into the current branch  
- `git rebase <branch_name>` – Reapply commits on top of another branch  

# Undo & Reset  
- `git reset --soft HEAD~1` – Undo last commit but keep changes staged  
- `git reset --hard HEAD~1` – Undo last commit and discard changes  
- `git revert <commit_hash>` – Create a new commit that undoes a previous commit  

# Remote & Syncing  
- `git remote -v` – View remote repository URLs  
- `git fetch --all` – Fetch changes from all remotes  
- `git pull origin <branch>` – Pull latest changes from remote  
- `git push origin <branch>` – Push local changes to remote  

# Stashing & Cleaning  
- `git stash` – Temporarily save changes  
- `git stash pop` – Apply stashed changes  
- `git clean -df` – Remove untracked files and directories  

# Logging & Searching  
- `git log --oneline --graph --decorate --all` – Pretty log output  
- `git grep "search_term"` – Search for a term in tracked files  
