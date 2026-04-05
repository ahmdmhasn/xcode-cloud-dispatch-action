# Xcode Cloud Dispatcher Action 🚀

A lightweight, professional GitHub Action to manually trigger **Xcode Cloud** builds for Flutter and Native iOS projects. It automatically detects your marketing version and returns a direct deep-link to the build summary in App Store Connect.

## Features

- 📱 **Universal Support:** Works out-of-the-box for Flutter (`pubspec.yaml`) and Native iOS (`MARKETING_VERSION`).
- 🔗 **Deep Linking:** Generates a direct URL to the specific build run (requires Team/App ID).
- 🔑 **Automated Auth:** Handles ES256 JWT generation for the App Store Connect API.
- 🛠 **Flexible:** Optionally provide a custom `project_path` or `marketing_version`.
- 💬 **PR Optimized:** Designed to update PR comments for a seamless developer experience.

---

## Usage

Create a workflow file (e.g., `.github/workflows/xcode_cloud.yml`) in your repository. This example triggers the build when a user comments `/build` on a Pull Request.

```yaml
name: Xcode Cloud Dispatch
on:
  issue_comment:
    types: [created]

jobs:
  dispatch:
    # Only run if it's a PR comment and the command is exactly /build
    if: github.event.issue.pull_request && github.event.comment.body == '/build'
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
        with:
          # Targets the PR branch head
          ref: ${{ format('refs/pull/{0}/head', github.event.issue.number) }}

      - name: Trigger Xcode Cloud
        id: xcode
        uses: your-username/xcode-cloud-dispatcher@v0.1
        with:
          apple_key_id: ${{ secrets.APPSTORE_KEY_ID }}
          apple_issuer_id: ${{ secrets.APPSTORE_ISSUER_ID }}
          apple_private_key: ${{ secrets.APPSTORE_PRIVATE_KEY }}
          workflow_id: ${{ vars.XCODE_CLOUD_WORKFLOW_ID }}
          # Providing these enables the deep-link output
          team_id: "your-team-uuid"
          app_id: "your-app-id"

      - name: Feedback to PR
        if: always()
        run: |
          VERSION="${{ steps.xcode.outputs.marketing_version }}"
          BUILD="${{ steps.xcode.outputs.build_number }}"
          URL="${{ steps.xcode.outputs.build_url }}"
          
          MSG="🚀 **Xcode Cloud Build Started**"
          if [[ -n "$VERSION" ]]; then MSG="$MSG\n**Version:** \`$VERSION\`"; fi
          MSG="$MSG\n**Build:** \`$BUILD\`\n\n[View Build Summary]($URL)"

          # Updates the original /build comment with the results
          gh comment edit "${{ github.event.comment.id }}" --body "${{ github.event.comment.body }}\n\n> $MSG"
        env:
          GH_TOKEN: "${{ secrets.GITHUB_TOKEN }}"
```

---

## Inputs

| Input | Description | Required | Default |
| :--- | :--- | :---: | :--- |
| `apple_key_id` | App Store Connect API Key ID (e.g., `2X9....`) | **Yes** | - |
| `apple_issuer_id` | App Store Connect Issuer ID (UUID) | **Yes** | - |
| `apple_private_key` | The content of your `.p8` private key file | **Yes** | - |
| `workflow_id` | The Xcode Cloud Workflow ID from App Store Connect | **Yes** | - |
| `project_path` | Path to your `.xcodeproj` (e.g., `ios/Runner.xcodeproj`) | No | Auto-detected |
| `team_id` | Your App Store Connect Team ID (UUID) | No | - |
| `app_id` | Your Apple App ID (10-digit number) | No | - |

## Outputs

| Output | Description |
| :--- | :--- |
| `build_number` | The integer build number assigned by Apple (e.g., `42`) |
| `marketing_version` | The version detected (e.g., `1.2.0`) |
| `build_url` | A direct link to the build summary or general dashboard |

---

## Setup Tips

1. **Private Key:** When adding your `APPLE_PRIVATE_KEY` to GitHub Secrets, paste the entire content including `-----BEGIN PRIVATE KEY-----` and `-----END PRIVATE KEY-----`.
2. **Workflow ID:** You can find this in App Store Connect under the "Xcode Cloud" tab in your App settings.
3. **Permissions:** Ensure your App Store Connect API Key has at least **Developer** or **App Manager** access.

## License

[MIT](LICENSE)