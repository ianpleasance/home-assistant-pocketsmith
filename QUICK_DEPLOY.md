# Quick Deployment Guide - From Archive to GitHub

This guide walks you through deploying your PocketSmith integration from the archive to a live GitHub repository.

## 📦 What You Have

- `pocketsmith_integration.tar.gz` - Complete integration archive
- All 26 files needed for a production-ready repository
- Fully documented and tested code

## 🚀 5-Step Deployment

### Step 1: Extract Archive (1 minute)

```bash
# Extract the archive
tar -xzf pocketsmith_integration.tar.gz

# Navigate to directory
cd pocketsmith_integration

# Verify contents
ls -la
```

You should see:
```
.github/
custom_components/
CHANGELOG.md
CONTRIBUTING.md
DEVELOPER.md
EXAMPLES.md
INSTALLATION.md
LICENSE
QUICKSTART.md
README.md
STRUCTURE.md
hacs.json
info.md
.gitignore
```

### Step 2: Initialize Git (2 minutes)

```bash
# Initialize repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial release v1.0.0

Features:
- UI-based configuration (no configuration.yaml needed)
- Account balance sensors with stable ID-based naming
- Transaction history sensors (last 20 transactions per account)
- Automatic updates every 5 minutes
- HACS compatible
- Complete documentation and examples
- Multi-currency support
- Rich attributes for accounts and transactions"

# Set main branch
git branch -M main
```

### Step 3: Create GitHub Repository (3 minutes)

**Option A: Via GitHub Website**

1. Go to https://github.com/new
2. Repository name: `home-assistant-pocketsmith`
3. Description: `PocketSmith integration for Home Assistant with UI configuration`
4. Public repository
5. Don't initialize with README (we have one)
6. Click "Create repository"

**Option B: Via GitHub CLI**

```bash
gh repo create home-assistant-pocketsmith --public --source=. --remote=origin --description="PocketSmith integration for Home Assistant"
```

### Step 4: Push to GitHub (1 minute)

```bash
# Add remote (if not using gh CLI)
git remote add origin https://github.com/YOUR_USERNAME/home-assistant-pocketsmith.git

# Push code
git push -u origin main
```

### Step 5: Create Release (2 minutes)

**Via GitHub Website:**

1. Go to your repository on GitHub
2. Click "Releases" → "Create a new release"
3. Tag: `v1.0.0`
4. Release title: `v1.0.0 - Initial Release`
5. Description: Copy from CHANGELOG.md
6. Click "Publish release"

**Via GitHub CLI:**

```bash
gh release create v1.0.0 --title "v1.0.0 - Initial Release" --notes-file CHANGELOG.md
```

## ✅ Deployment Complete!

Your repository is now live at:
`https://github.com/YOUR_USERNAME/home-assistant-pocketsmith`

## 🎯 Next Steps

### Immediate (Do Now)

1. **Add Repository Topics**
   - Go to repository → "About" section → "Add topics"
   - Add: `home-assistant`, `hacs`, `pocketsmith`, `integration`, `custom-component`, `finance`

2. **Enable Issues**
   - Settings → Features → Check "Issues"

3. **Verify Files**
   - Click through files on GitHub
   - Ensure all rendered correctly
   - Check that images/links work

4. **Test Installation**
   - Install via HACS custom repository
   - Verify sensors appear
   - Test with real API key

### Short-term (This Week)

5. **Add to HACS Custom Repository**
   Users can now install via:
   - HACS → Integrations → ⋮ menu → Custom repositories
   - URL: `https://github.com/YOUR_USERNAME/home-assistant-pocketsmith`
   - Category: Integration

6. **Announce in Community**
   - Post in [Home Assistant Community](https://community.home-assistant.io/)
   - Post in [r/homeassistant](https://reddit.com/r/homeassistant)
   - Share on social media

7. **Monitor Issues**
   - Respond to questions
   - Fix reported bugs
   - Thank contributors

### Long-term (Optional)

8. **Submit to HACS Default**
   - After 2-3 weeks of testing
   - Submit PR to [hacs/default](https://github.com/hacs/default)
   - Follow HACS submission guidelines

9. **Set Up GitHub Actions**
   - Already included in `.github/workflows/validate.yaml`
   - Should run automatically on push/PR

10. **Add Documentation Site** (Optional)
    - GitHub Pages
    - ReadTheDocs
    - Dedicated documentation site

## 📝 Post-Deployment Checklist

- [ ] Repository created on GitHub
- [ ] All files pushed successfully
- [ ] v1.0.0 release created
- [ ] Repository topics added
- [ ] Issues enabled
- [ ] GitHub Actions workflow running
- [ ] README renders correctly
- [ ] Links in README work
- [ ] Installation tested via HACS
- [ ] Sensors appear after configuration
- [ ] Can see friendly names
- [ ] Transaction data loads
- [ ] Documentation reviewed

## 🎨 Customization (Optional)

### Update Repository URLs

If you want to customize repository name or username, update these files:

```bash
# Update README.md
sed -i 's/cloudbr34k84/YOUR_USERNAME/g' README.md

# Update INSTALLATION.md
sed -i 's/cloudbr34k84/YOUR_USERNAME/g' INSTALLATION.md

# Update other docs if needed
```

### Add Repository Banner

Create a banner image and add to README:

```markdown
![PocketSmith Integration](images/banner.png)
```

### Add Badges

Add to top of README.md:

```markdown
[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)
[![hacs][hacsbadge]][hacs]

[releases-shield]: https://img.shields.io/github/release/YOUR_USERNAME/home-assistant-pocketsmith.svg
[releases]: https://github.com/YOUR_USERNAME/home-assistant-pocketsmith/releases
[commits-shield]: https://img.shields.io/github/commit-activity/y/YOUR_USERNAME/home-assistant-pocketsmith.svg
[commits]: https://github.com/YOUR_USERNAME/home-assistant-pocketsmith/commits/main
[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg
[license-shield]: https://img.shields.io/github/license/YOUR_USERNAME/home-assistant-pocketsmith.svg
```

## 🐛 Troubleshooting

### "Permission denied" when pushing

```bash
# Use HTTPS with token or SSH
git remote set-url origin git@github.com:YOUR_USERNAME/home-assistant-pocketsmith.git
```

### GitHub Actions failing

- Check `.github/workflows/validate.yaml` syntax
- Ensure you have GitHub Actions enabled
- Review logs in Actions tab

### HACS validation failing

- Verify `hacs.json` is valid JSON
- Check `manifest.json` has required fields
- Ensure `info.md` exists

### Files not showing correctly

- Check file encodings are UTF-8
- Verify line endings (use LF, not CRLF)
- Ensure no hidden characters

## 💡 Tips for Success

1. **Respond Quickly** - Answer issues within 24-48 hours
2. **Be Welcoming** - Thank people for feedback
3. **Document Changes** - Update CHANGELOG.md for each version
4. **Test Before Release** - Always test locally first
5. **Use Semantic Versioning** - 1.0.0 → 1.1.0 → 2.0.0
6. **Keep Documentation Updated** - Update README when adding features
7. **Engage Community** - Ask for feedback and suggestions

## 📊 Success Metrics

Track these to measure adoption:

- **GitHub Stars** - Indicates popularity
- **Issues/PRs** - Shows engagement
- **HACS Installs** - Direct usage metric
- **Community Posts** - Forum discussions
- **Contributors** - Community involvement

## 🎉 Congratulations!

Your integration is now:
- ✅ Live on GitHub
- ✅ Available for installation
- ✅ Documented comprehensively
- ✅ Ready for users
- ✅ Open for contributions

## 🆘 Need Help?

If you run into issues:

1. Check the [GitHub Docs](https://docs.github.com)
2. Review [HACS Docs](https://hacs.xyz)
3. Ask in [HA Community](https://community.home-assistant.io)
4. Open an issue in the repository

## 📚 Additional Resources

- [Home Assistant Developer Docs](https://developers.home-assistant.io/)
- [HACS Integration Guide](https://hacs.xyz/docs/publish/integration)
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Semantic Versioning](https://semver.org/)

---

**Ready to deploy?** Follow the 5 steps above and you'll be live in ~10 minutes! 🚀
