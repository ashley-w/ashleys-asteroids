# Deployment Setup for GitHub Actions + Netlify

This project now uses GitHub Actions to build the game and deploy to Netlify automatically.

## Setup Steps:

### 1. Get Netlify Tokens
1. Go to [Netlify](https://app.netlify.com)
2. Go to **User Settings** → **Applications** → **Personal access tokens**
3. Create a new token, copy it (this is your `NETLIFY_AUTH_TOKEN`)
4. Go to your site → **Site Settings** → **General** → **Site details**
5. Copy your **Site ID** (this is your `NETLIFY_SITE_ID`)

### 2. Add GitHub Secrets
1. Go to your GitHub repo → **Settings** → **Secrets and variables** → **Actions**
2. Add these Repository Secrets:
   - `NETLIFY_AUTH_TOKEN`: Your personal access token from step 1
   - `NETLIFY_SITE_ID`: Your site ID from step 1

### 3. Push Changes
```bash
git add .
git commit -m "Set up GitHub Actions deployment"
git push
```

### 4. Watch the Magic
- GitHub Actions will automatically build your game
- Then deploy it to Netlify
- Check the **Actions** tab in your GitHub repo to see the build progress

## How It Works:
1. **Push to main branch** triggers the GitHub Action
2. **GitHub Actions** builds the game using pygbag in a clean Python environment
3. **Netlify deployment** happens automatically via the GitHub Action
4. **Your game goes live** at your Netlify URL

## Benefits:
- ✅ Reliable Python environment (no more dependency issues)
- ✅ Faster builds (GitHub Actions has better caching)
- ✅ Build logs are easier to debug
- ✅ Works with any Python version/dependencies
- ✅ Automatic deployment on every push