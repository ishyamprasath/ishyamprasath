# Maintaining this profile

This repository matches the GitHub username `ishyamprasath`, so GitHub displays its root README on the profile when the repository is public and the README is on the default branch.

The artwork is original, self-contained SVG with light and dark themes. The hero includes a portrait cutout prepared from the supplied photograph, embedded as PNG data inside each SVG. No external fonts, image hosts, stats services, API keys, or Python packages are required. GitHub renders the SVGs as images; the contact and repository links live in the README so they remain clickable.

The developer ID is decorative, with a floating 3D tilt, holographic sweep, and moving border. A portrait-format variant keeps the ID legible on mobile screens. The desktop terminal cycles through three areas of work. Project cards and toolkit panels gently float; circuit traces and the contribution snake also animate. Everything runs as image-safe CSS animation, without JavaScript, external resources, or hover interactions. `prefers-reduced-motion` stops the animations and leaves the first terminal message visible. The card is a personal developer badge, not an institutional ID.

## Update the content

Edit `README.md` for the biography, experience, skills, and links. Edit `profile/profile.json` for the project cards and identity. Replace `assets/portrait.png` to update the portrait. Hero copy, artwork, animation, and the toolkit visual live in `scripts/generate_profile.py`.

From the repository root, run:

```sh
python3 -m unittest discover -s tests -v
python3 scripts/generate_profile.py --refresh
```

The generator downloads only the public contribution calendar from `https://github.com/users/ishyamprasath/contributions`, checks it, saves `profile/contributions.json`, and generates ten SVGs in `assets/`. It does not access private contribution details. Counts reflect what GitHub exposes publicly, including anonymized private counts if the account owner has enabled them. The displayed range follows GitHub's calendar and may include a partial extra week. Longest streak and active days apply to the displayed range, not the account's lifetime.

To regenerate the images without network access, use the saved snapshot:

```sh
python3 scripts/generate_profile.py
```

Refresh errors fail visibly rather than replacing real data with invented or empty statistics. Existing images remain available if a scheduled update fails. The snapshot date is shown in each activity card. The snake animation sweeps the actual calendar cells in alternating column directions; its movement is decorative, and contribution values come from GitHub.

## Automatic refresh

`.github/workflows/refresh-profile.yml` refreshes activity daily at 00:30 UTC, supports manual runs, and regenerates artwork when its source changes. It uses the repository's built-in `GITHUB_TOKEN` with `contents: write` to commit only generated artwork and the contribution snapshot to the default branch. No personal access token is needed. The checkout action is pinned to a full commit SHA.

Once the files are pushed, run **Actions → Refresh profile → Run workflow** to verify the automation on GitHub. GitHub must allow Actions and workflow writes to this repository. If a branch rule blocks bot pushes, use the local refresh command and commit the generated files through the repository's normal review process. Scheduled workflows can be delayed or disabled by GitHub after prolonged repository inactivity; re-enable or run manually as needed.

## Publishing

Commit these files and push to the repository's default branch. A live profile and a successful hosted workflow run must be verified on GitHub after publishing; local rendering alone does not establish either.

The updated `Shyam_Prasath_S_Resume.pdf` was used as source material, with no PDF or phone number included. Employer projects are described without inventing source-code URLs. Education uses the resume's specific **Micro Credit Program in Computer Science** title. Techobytes Technologies × eDC IIT Delhi is identified as the robotics training organizer; IIT Madras Research Park is the venue.
