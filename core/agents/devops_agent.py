"""
DevOps Agent - Manages git workflow, branches, and code quality

One of the Wisdom Council characters manages:
- Branch strategy (dev/main workflow)
- Code quality checks
- Deployment readiness
- Git workflow enforcement
"""

import subprocess
from typing import Dict, List, Any
from pathlib import Path


class DevOpsAgent:
    """Manages DevOps and git workflow for projects."""

    def __init__(self, project_path: str):
        """Initialize DevOps agent."""
        self.project_path = Path(project_path)
        self.repo = self._init_repo()
        self.status = {
            "current_branch": None,
            "branches": [],
            "uncommitted_changes": False,
            "remote_status": None,
            "code_quality": {}
        }

    def _init_repo(self):
        """Initialize git repository reference."""
        try:
            import git
            return git.Repo(self.project_path)
        except Exception as e:
            print(f"⚠️  Could not initialize git repo: {e}")
            return None

    def analyze_workflow(self) -> Dict[str, Any]:
        """Analyze current git workflow status."""
        print("\n" + "=" * 70)
        print("🚀 DEVOPS ANALYSIS - Git Workflow & Code Quality")
        print("=" * 70)

        try:
            # Get current branch
            if self.repo:
                self.status["current_branch"] = self.repo.active_branch.name

            # List branches
            self._analyze_branches()

            # Check for uncommitted changes
            self._check_uncommitted_changes()

            # Check remote status
            self._check_remote_status()

            # Check code quality
            self._check_code_quality()

            return self.status

        except Exception as e:
            print(f"⚠️  DevOps analysis error: {e}")
            return self.status

    def _analyze_branches(self):
        """Analyze branch structure."""
        print("\n📊 Branch Analysis")
        print("-" * 70)

        if not self.repo:
            print("⚠️  Git repo not available")
            return

        try:
            branches = [ref.name.split('/')[-1] for ref in self.repo.heads]
            self.status["branches"] = branches

            has_dev = "dev" in branches or "develop" in branches
            has_main = "main" in branches or "master" in branches

            print(f"Current branch: {self.status['current_branch']}")
            print(f"Total branches: {len(branches)}")
            print(f"Dev branch: {'✅' if has_dev else '❌'}")
            print(f"Main branch: {'✅' if has_main else '❌'}")

            if not has_dev:
                print("\n⚠️  RECOMMENDATION: Create 'dev' branch for development")
            if not has_main:
                print("\n⚠️  RECOMMENDATION: Ensure 'main' branch exists")

        except Exception as e:
            print(f"⚠️  Could not analyze branches: {e}")

    def _check_uncommitted_changes(self):
        """Check for uncommitted changes."""
        print("\n📝 Uncommitted Changes")
        print("-" * 70)

        if not self.repo:
            print("⚠️  Git repo not available")
            return

        try:
            untracked = len(self.repo.untracked_files)
            uncommitted = len(self.repo.index.diff(self.repo.head.commit))

            if untracked > 0 or uncommitted > 0:
                print(f"⚠️  Uncommitted changes detected:")
                print(f"   - Untracked files: {untracked}")
                print(f"   - Modified files: {uncommitted}")
                self.status["uncommitted_changes"] = True

                if self.repo.active_branch.name != "dev" and self.repo.active_branch.name != "develop":
                    print(f"\n⚠️  RECOMMENDATION: Commit changes or switch to 'dev' branch")
            else:
                print("✅ All changes committed")
                self.status["uncommitted_changes"] = False

        except Exception as e:
            print(f"⚠️  Could not check changes: {e}")

    def _check_remote_status(self):
        """Check remote tracking status."""
        print("\n🌐 Remote Status")
        print("-" * 70)

        if not self.repo or not self.repo.remotes:
            print("⚠️  No remote configured")
            return

        try:
            remote = self.repo.remote()
            ahead = 0
            behind = 0

            try:
                # Get tracking branch
                tracking_branch = self.repo.active_branch.tracking_branch()
                if tracking_branch:
                    commits_ahead = list(self.repo.iter_commits(
                        f"{tracking_branch}..HEAD"
                    ))
                    commits_behind = list(self.repo.iter_commits(
                        f"HEAD..{tracking_branch}"
                    ))
                    ahead = len(commits_ahead)
                    behind = len(commits_behind)
            except:
                pass

            if ahead > 0:
                print(f"⚠️  Local branch is {ahead} commits ahead")
                print(f"   RECOMMENDATION: Push to remote with: git push")

            if behind > 0:
                print(f"⚠️  Local branch is {behind} commits behind")
                print(f"   RECOMMENDATION: Pull from remote with: git pull")

            if ahead == 0 and behind == 0:
                print("✅ Local and remote are in sync")

            self.status["remote_status"] = {
                "ahead": ahead,
                "behind": behind,
                "in_sync": ahead == 0 and behind == 0
            }

        except Exception as e:
            print(f"⚠️  Could not check remote: {e}")

    def _check_code_quality(self):
        """Check basic code quality metrics."""
        print("\n✨ Code Quality")
        print("-" * 70)

        try:
            # Count Python files
            py_files = list(self.project_path.glob("**/*.py"))
            py_files = [f for f in py_files if ".venv" not in str(f) and "__pycache__" not in str(f)]

            # Check for common issues
            issues = {
                "has_tests": False,
                "has_docs": False,
                "has_readme": False,
                "has_gitignore": False,
                "has_requirements": False
            }

            # Check for test directory
            if any(d.name in ["tests", "test"] for d in self.project_path.iterdir() if d.is_dir()):
                issues["has_tests"] = True

            # Check for documentation
            if (self.project_path / "docs").exists():
                issues["has_docs"] = True

            # Check for README
            if (self.project_path / "README.md").exists() or (self.project_path / "README.rst").exists():
                issues["has_readme"] = True

            # Check for .gitignore
            if (self.project_path / ".gitignore").exists():
                issues["has_gitignore"] = True

            # Check for requirements.txt or setup.py
            if (self.project_path / "requirements.txt").exists() or (self.project_path / "setup.py").exists():
                issues["has_requirements"] = True

            print(f"Python files: {len(py_files)}")
            print(f"Tests: {'✅' if issues['has_tests'] else '❌'}")
            print(f"Documentation: {'✅' if issues['has_docs'] else '❌'}")
            print(f"README: {'✅' if issues['has_readme'] else '❌'}")
            print(f".gitignore: {'✅' if issues['has_gitignore'] else '❌'}")
            print(f"Requirements: {'✅' if issues['has_requirements'] else '❌'}")

            self.status["code_quality"] = issues

            # Recommendations
            missing = [k for k, v in issues.items() if not v]
            if missing:
                print(f"\n📋 RECOMMENDATIONS:")
                if not issues["has_readme"]:
                    print(f"   • Add README.md with project description")
                if not issues["has_tests"]:
                    print(f"   • Create tests/ directory with unit tests")
                if not issues["has_docs"]:
                    print(f"   • Create docs/ directory with documentation")
                if not issues["has_gitignore"]:
                    print(f"   • Add .gitignore file")
                if not issues["has_requirements"]:
                    print(f"   • Add requirements.txt or setup.py")

        except Exception as e:
            print(f"⚠️  Could not check code quality: {e}")

    def get_workflow_recommendations(self) -> List[str]:
        """Get DevOps workflow recommendations."""
        recommendations = []

        # Branch recommendations
        if self.status["current_branch"] not in ["dev", "develop"]:
            if self.status["uncommitted_changes"]:
                recommendations.append(
                    "Switch to 'dev' branch before making changes: git checkout -b dev"
                )

        # Remote recommendations
        if self.status.get("remote_status"):
            remote = self.status["remote_status"]
            if remote.get("ahead", 0) > 0:
                recommendations.append(f"Push {remote['ahead']} commits: git push origin {self.status['current_branch']}")
            if remote.get("behind", 0) > 0:
                recommendations.append(f"Pull {remote['behind']} commits: git pull origin {self.status['current_branch']}")

        # Code quality recommendations
        quality = self.status.get("code_quality", {})
        if not quality.get("has_tests"):
            recommendations.append("Add unit tests in tests/ directory")
        if not quality.get("has_docs"):
            recommendations.append("Add documentation in docs/ directory")

        return recommendations

    def suggest_release_readiness(self) -> Dict[str, Any]:
        """Check if project is ready for release to main branch."""
        ready = True
        checklist = []

        print("\n" + "=" * 70)
        print("📦 RELEASE READINESS CHECK")
        print("=" * 70)

        # Check 1: On main/master branch
        if self.status["current_branch"] not in ["main", "master"]:
            ready = False
            checklist.append({
                "item": f"Currently on '{self.status['current_branch']}' branch",
                "status": "❌ Switch to main: git checkout main",
                "required": True
            })
        else:
            checklist.append({
                "item": "On main branch",
                "status": "✅",
                "required": True
            })

        # Check 2: No uncommitted changes
        if self.status["uncommitted_changes"]:
            ready = False
            checklist.append({
                "item": "No uncommitted changes",
                "status": "❌ Commit or stash changes first",
                "required": True
            })
        else:
            checklist.append({
                "item": "No uncommitted changes",
                "status": "✅",
                "required": True
            })

        # Check 3: In sync with remote
        remote = self.status.get("remote_status", {})
        if remote.get("in_sync"):
            checklist.append({
                "item": "In sync with remote",
                "status": "✅",
                "required": True
            })
        else:
            ready = False
            checklist.append({
                "item": "In sync with remote",
                "status": f"❌ {remote.get('ahead', 0)} ahead, {remote.get('behind', 0)} behind",
                "required": True
            })

        # Check 4: Has tests
        quality = self.status.get("code_quality", {})
        if quality.get("has_tests"):
            checklist.append({
                "item": "Tests present",
                "status": "✅",
                "required": False
            })
        else:
            checklist.append({
                "item": "Tests present",
                "status": "⚠️  No tests found",
                "required": False
            })

        # Check 5: Has documentation
        if quality.get("has_docs"):
            checklist.append({
                "item": "Documentation present",
                "status": "✅",
                "required": False
            })
        else:
            checklist.append({
                "item": "Documentation present",
                "status": "⚠️  No docs found",
                "required": False
            })

        print(f"\nRelease Readiness: {'🟢 READY' if ready else '🔴 NOT READY'}\n")

        for check in checklist:
            print(f"{check['status']}")
            print(f"   {check['item']}\n")

        return {
            "ready": ready,
            "checklist": checklist,
            "recommendation": "Safe to release to main" if ready else "Address failing checks before release"
        }
