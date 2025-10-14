# 🔒 Security Fix: Removing API Keys from Git

## ⚠️ Important: API Key Exposed!

GitHub detected that your Groq API key was committed to the repository. This is a **security risk** because anyone can see and use your API key.

---

## ✅ What I've Done to Fix This

### 1. Created `.gitignore` ✅
Added `ai_config.json` to `.gitignore` so it won't be tracked by Git in the future.

### 2. Created Template Files ✅
- `ai_config.json.template` - Safe template without real API key
- `.env.example` - Example environment variables file

### 3. Removed API Key from Config ✅
Cleared the API key from `ai_config.json` (your local file still needs it - see below)

---

## 🚨 CRITICAL: What You Need to Do Now

### Step 1: Revoke Your Current API Key 🔑

**Your exposed API key**: `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`

1. Go to: https://console.groq.com
2. Log in to your account
3. Navigate to **API Keys** section
4. **Delete** the exposed key: `gsk_6R0UMd...Tnpx`
5. **Generate a new API key**
6. Copy the new key

### Step 2: Set Up Your Local Environment 🖥️

Choose **Option A** (Recommended) or **Option B**:

#### Option A: Use Environment Variable (Recommended) ✅

```bash
# Create .env file
echo "GROQ_API_KEY=your_new_api_key_here" > .env

# Or add to your shell profile (~/.zshrc or ~/.bashrc)
echo 'export GROQ_API_KEY="your_new_api_key_here"' >> ~/.zshrc
source ~/.zshrc
```

The app will automatically read from `GROQ_API_KEY` environment variable.

#### Option B: Use Config File (Local Only) ⚠️

```bash
# Copy template and add your new key
cp ai_config.json.template ai_config.json

# Edit ai_config.json and add your NEW API key
# Replace "YOUR_API_KEY_HERE" with your new key
```

**Important**: The `ai_config.json` file is now in `.gitignore`, so it won't be committed to Git.

### Step 3: Remove History from Git 🗑️

The old API key is still in Git history. You need to remove it:

#### Method 1: Using BFG Repo-Cleaner (Recommended)

```bash
# Install BFG
# On Ubuntu/Debian:
sudo apt install bfg

# On macOS:
brew install bfg

# Clean the repository
cd /home/omindu/Documents/Python/student_streess_ML
bfg --replace-text <(echo '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==>REMOVED')

# Clean up
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

#### Method 2: Using git filter-branch

```bash
cd /home/omindu/Documents/Python/student_streess_ML

# Remove the file from history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch ai_config.json" \
  --prune-empty --tag-name-filter cat -- --all

# Clean up
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

#### Method 3: Start Fresh (Easiest if repo is new)

```bash
# Remove .git directory
cd /home/omindu/Documents/Python/student_streess_ML
rm -rf .git

# Initialize new repository
git init
git add .
git commit -m "Initial commit (with security fixes)"
```

### Step 4: Force Push to GitHub 🚀

After cleaning the history:

```bash
# Add remote (if starting fresh)
git remote add origin https://github.com/OminduD/student_streess_ML.git

# Force push to overwrite history
git push origin master --force

# If you have other branches
git push origin --all --force
git push origin --tags --force
```

---

## 📋 Setup Instructions for New Users

Add this to your README:

### Setting Up API Keys

1. **Get a Groq API Key**:
   - Visit https://console.groq.com
   - Sign up for a free account
   - Generate an API key

2. **Configure the Application**:

   **Option A: Environment Variable (Recommended)**
   ```bash
   export GROQ_API_KEY="your_api_key_here"
   ```

   **Option B: Config File**
   ```bash
   cp ai_config.json.template ai_config.json
   # Edit ai_config.json and add your API key
   ```

3. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

---

## 🔒 Security Best Practices

### ✅ DO:
- Use environment variables for API keys
- Keep `ai_config.json` in `.gitignore`
- Revoke exposed API keys immediately
- Use `.env` files (and add to `.gitignore`)
- Share template files (`.template`, `.example`)

### ❌ DON'T:
- Commit API keys to Git
- Share API keys in public repos
- Store secrets in code files
- Push `.env` files to GitHub
- Ignore security warnings from GitHub

---

## 🧪 Verify Security

### Check what will be committed:
```bash
# This should NOT show ai_config.json or .env
git status

# Check .gitignore is working
git check-ignore ai_config.json
# Should output: ai_config.json

# Search for any remaining keys
git grep -i "gsk_" 
# Should return nothing (or only template files)
```

### Check GitHub doesn't have the key:
```bash
# After pushing, verify on GitHub:
# 1. Go to your repo
# 2. Search for "gsk_" 
# 3. Should only find template files
```

---

## 📚 Files Updated

### New Files (Safe to Commit):
- ✅ `.gitignore` - Prevents committing secrets
- ✅ `ai_config.json.template` - Template without real key
- ✅ `.env.example` - Example environment variables
- ✅ `SECURITY_FIX.md` - This guide

### Modified Files:
- ✅ `ai_config.json` - API key removed (now in `.gitignore`)

### Your Local Copy:
- ⚠️ Keep `ai_config.json` with your NEW API key (won't be committed)
- ⚠️ Or use `.env` file with `GROQ_API_KEY` (won't be committed)

---

## 🚨 Summary Checklist

- [ ] Revoke old API key on Groq console
- [ ] Generate new API key
- [ ] Set up environment variable or update local config
- [ ] Remove API key from Git history (choose method above)
- [ ] Verify `.gitignore` is working
- [ ] Force push cleaned repository to GitHub
- [ ] Verify key is not visible on GitHub
- [ ] Test app still works with new key

---

## 🆘 If You Need Help

### GitHub Still Shows Warning?
1. Make sure you removed the key from Git history
2. Force pushed the changes
3. Refreshed the GitHub page

### App Not Working?
```bash
# Check environment variable is set
echo $GROQ_API_KEY

# Or check config file
cat ai_config.json

# Test the connection
python test_groq.py
```

### Still Confused?
1. Follow "Method 3: Start Fresh" above (easiest)
2. Make sure to revoke the old key first!
3. Set up new key with environment variable

---

## 🎓 Learn More

- [GitHub: Removing sensitive data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
- [Git: filter-branch](https://git-scm.com/docs/git-filter-branch)
- [BFG Repo-Cleaner](https://rtyley.github.io/bfg-repo-cleaner/)
- [Groq API Documentation](https://console.groq.com/docs)

---

## ✨ After Fixing

Once you've completed all steps:

1. Your repository is secure ✅
2. API key is not in Git history ✅
3. New users can safely clone and set up ✅
4. Your app still works with the new key ✅

**You're all set! Your repository is now secure! 🔒**
