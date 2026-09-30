---
name: command-line-tool-development
description: "Use when designing or implementing a command-line program, subcommand, or shell-facing interface to specify arguments, input sources, output streams, exit codes, configuration precedence, and destructive-action safeguards before expanding functionality. Trigger for CLI creation, command changes, scripting interfaces, or terminal automation."
---

# Command-Line Tool Development

## Overview

This skill applies when designing or implementing a command-line program, subcommand, or shell-facing interface. Its intended outcome is to specify arguments, input sources, output streams, exit codes, configuration precedence, and destructive-action safeguards before expanding functionality.

## When to Use

### Preserved source section: When to Use

Use when people or scripts invoke a program through a terminal. Treat command names, flags, output, and exit status as a public interface that automation may depend on.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs

- Intended users, common tasks, operating systems, and shell environments.
- Commands, arguments, configuration sources, expected output, and error cases.
- Whether commands can overwrite, delete, publish, or otherwise change external state.

## Instructions

### Preserved source section: Procedure

1. **Define the interface.** Specify command grammar, required and optional arguments, defaults, environment/config precedence, and help text. Keep safe defaults and make ambiguous inputs fail clearly.
2. **Separate parsing from effects.** Parse and validate arguments before opening files, making network calls, or changing state. Expose core behavior as testable functions where practical.
3. **Make automation predictable.** Use stable exit codes, machine-readable output when requested, stdout for results, stderr for diagnostics, and no progress noise in quiet or JSON modes.
4. **Protect side effects.** Preview changes or require an explicit destructive flag for irreversible operations. Confirm destination paths and avoid following unexpected symlinks or glob expansions.
5. **Handle interruption and errors.** Clean up temporary files, preserve partial data deliberately, respond to signals, and return actionable messages without leaking secrets.
6. **Test at two levels.** Unit-test parsing and behavior; run subprocess tests for quoting, exit codes, streams, environment variables, working directories, and failure conditions.
7. **Document compatibility.** Keep help, examples, completion scripts, and migration notes aligned with the actual interface.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Inputs

- Whether commands can overwrite, delete, publish, or otherwise change external state.

### Source conditional guidance from: Procedure

3. **Make automation predictable.** Use stable exit codes, machine-readable output when requested, stdout for results, stderr for diagnostics, and no progress noise in quiet or JSON modes.

### Source conditional guidance from: Output and Acceptance

Report the command contract, defaults, exit behavior, side-effect gates, supported environments, and tested invocations. Accept when a human can discover the interface and a script can reliably distinguish success, expected failure, and unexpected failure.

## Output Format

### Preserved source section: Output and Acceptance

Report the command contract, defaults, exit behavior, side-effect gates, supported environments, and tested invocations. Accept when a human can discover the interface and a script can reliably distinguish success, expected failure, and unexpected failure.

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Edge Cases and Recovery

### Source edge/failure guidance from: Inputs

- Commands, arguments, configuration sources, expected output, and error cases.

### Source edge/failure guidance from: Procedure

1. **Define the interface.** Specify command grammar, required and optional arguments, defaults, environment/config precedence, and help text. Keep safe defaults and make ambiguous inputs fail clearly.
5. **Handle interruption and errors.** Clean up temporary files, preserve partial data deliberately, respond to signals, and return actionable messages without leaking secrets.
6. **Test at two levels.** Unit-test parsing and behavior; run subprocess tests for quoting, exit codes, streams, environment variables, working directories, and failure conditions.

### Source edge/failure guidance from: Output and Acceptance

Report the command contract, defaults, exit behavior, side-effect gates, supported environments, and tested invocations. Accept when a human can discover the interface and a script can reliably distinguish success, expected failure, and unexpected failure.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Acceptance criteria from source: Output and Acceptance

Report the command contract, defaults, exit behavior, side-effect gates, supported environments, and tested invocations. Accept when a human can discover the interface and a script can reliably distinguish success, expected failure, and unexpected failure.
