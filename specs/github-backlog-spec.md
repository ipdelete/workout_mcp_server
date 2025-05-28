# GitHub Backlog Creation Spec

## High level objectives
Create a comprehensive GitHub issue backlog for the Workout MCP Server project, organizing all tasks from the project backlog into trackable GitHub issues using the proper issue template.

## Mid-level objectives
1. Convert each task from the project backlog into a GitHub issue
2. Organize issues by development phase (1-5)
3. Include relevant MCP implementation details for each task
4. Use the GitHub Task issue template for consistency
5. Add proper labels and metadata to issues

## Implementation Notes

### Issue Structure
Each issue should include:
- Clear title indicating the phase and task
- Description with implementation details
- Acceptance criteria
- Technical notes from MCP documentation where relevant
- Dependencies on other tasks

### MCP-Specific Details to Include:
- **For Phase 1**: Note that FastMCP is the chosen framework (per ADR-002)
- **For Phase 2**: Mention the JSON data structure requirements
- **For Phase 3**: Reference MCP tool implementation patterns
- **For Phase 4**: Include fitness calculation formulas (CTL, ATL, TSB)
- **For Phase 5**: Note testing approach from ADR-001

### GitHub CLI Commands
Use `gh issue create` with the Task template:
- `--title` for the task name
- `--body` for detailed description
- `--label` for phase and type labels

## Task List
1. Create Phase 1 issues (3 tasks)
   - Project directory structure
   - Python environment setup
   - MCP server skeleton
2. Create Phase 2 issues (2 tasks)
   - Generate mock workout data
   - Data loading functionality
3. Create Phase 3 issues (3 tasks)
   - get_workout_by_id tool
   - get_last_7_workouts tool
   - get_last_50_workouts tool
4. Create Phase 4 issues (3 tasks)
   - Fitness calculation (CTL)
   - Fatigue calculation (ATL)
   - Form calculation (TSB)
5. Create Phase 5 issues (3 tasks)
   - Register tools with MCP server
   - Test server functionality
   - Error handling and edge cases

Remember ONLY CREATE issues/tasks using gh cli, don't try to do any of the work.