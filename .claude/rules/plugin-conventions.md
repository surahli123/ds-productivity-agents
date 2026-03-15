# Skill Development Conventions

> **Note:** This repository is structured as a Claude Code plugin skill set (`ds-productivity`).
> Skills live under `skills/`, commands under `.claude/commands/`, and the plugin manifest at `.claude-plugin/`.

## File Organization

### Skills
- Each skill lives in `skills/[skill-name]/`
- Skill definition in `SKILL.md` within that directory (required)
- Companion files co-located in the skill directory or under `references/`
- Use frontmatter for metadata:
  ```yaml
  ---
  name: skill-name
  description: What this skill does and when to trigger it
  ---
  ```

### Skill References
- Subagent prompts, rubrics, and data files go in `skills/[skill-name]/references/`
- Domain digests go in `skills/[skill-name]/digests/` (for domain knowledge skills)
- Reference files are loaded on demand, not auto-injected into context

### Commands
- Project commands go in `.claude/commands/` (auto-discovered by Claude Code)
- Commands should be thin — delegate to SKILL.md for logic
- Use frontmatter for configuration:
  ```yaml
  ---
  description: What this command does
  argument-hint: [arg1] [--flag]
  model: opus
  ---
  ```

### Plugin Manifest
- `.claude-plugin/plugin.json` at project root — for future marketplace publishing
- Not required for project-level functionality (commands work without it)

## Path Resolution

### Within a Skill
- Use **skill-relative paths**: `references/framework.md`, `digests/search-ranking.md`
- These resolve relative to the SKILL.md directory

### Cross-Skill References
- Use **project-relative paths**: `skills/search-domain-knowledge/digests/{domain}.md`
- The command and orchestrator run in project context, so project-relative paths work

### Subagent Dispatch
- Subagents inherit the project working directory
- Use project-relative paths in dispatch payloads: `skills/ds-review/references/analysis-reviewer.md`

## Skill Prompts

### Structure
1. **Role**: What is this skill/agent's job?
2. **Context**: What does it need to know?
3. **Process**: Step-by-step instructions
4. **Output Format**: What should the output look like?
5. **Examples**: Reference examples if helpful

### Best Practices
- Be specific about what the skill should do
- Include examples of good output
- Define clear output format (markdown templates work well)
- Specify when to use subagents vs handle directly
- Include error handling (what to do when input is unclear)

## Skill Design

### SKILL.md vs References
- SKILL.md contains the **workflow/orchestration logic** (the "how")
- References contain **data and prompts** (rubrics, reviewer instructions, domain knowledge)
- SKILL.md should be under 500 lines — split into references if larger

### What Goes in References
- Evaluation rubrics and scoring guidelines
- Subagent prompt definitions
- Persona definitions
- Domain-specific knowledge (digests)
- Example outputs

### What Stays in SKILL.md
- Orchestration pipeline (step-by-step process)
- Input parsing and mode branching
- Output format templates
- Rules and constraints

## Testing

Before considering a skill "done":
1. Test with at least 3 different inputs
2. Verify output format is consistent
3. Check that it handles unclear/incomplete input gracefully
4. Validate that references are loaded correctly
5. Run calibration baseline comparison (if scoring system exists)

## Version Control

- Keep `skills/` clean (only shipping code)
- Use `dev/` for work-in-progress, notes, scratch files
- Update CHANGELOG.md when shipping features
- Create ADRs for architectural decisions
