# setup — create a GTM home

Create the GTM home scaffold in a resolved location without overwriting anything.

## Use when

- No GTM home exists and the person wants one, or `onboard` needs somewhere to write.
- The person explicitly asks for a separate home (a second product line, a client engagement).

## Not when

- There is already a workspace with its own structure (a client Notion export, an existing GTM brain repo). Offer to map onto it instead.
- The person just wants one email written. Do the email.

## Steps

1. Resolve the destination. Use a path the person named, or ask once: "Where should the GTM home live? A folder name is enough." Default suggestion: `gtm-home/` in the current workspace. For agencies and consultants, one home per client: `clients/<client>/gtm-home/`.
2. Check what already exists at that path. List any files that would collide.
3. Create the scaffold:
   - With a shell: `python scripts/create_home.py <path>` (add `--with-accounts` or `--with-field` when relevant). The script never overwrites.
   - Without a shell: copy each file from `references/templates/` into the destination with the file tools.
   - Without a file system (plain chat): produce the six home files as one Markdown document or artifact and say that is the home for now. Skip the README there.
4. Fill only what is already known from the conversation — the company name, what it sells — and leave the rest as the template's prompts.
5. Hand off to `onboard`.

## Output

The created tree, a one-line note on what each file is for, and the first question `onboard` will ask.

## Could compound

Nothing yet. Setup creates the place lessons will go.
