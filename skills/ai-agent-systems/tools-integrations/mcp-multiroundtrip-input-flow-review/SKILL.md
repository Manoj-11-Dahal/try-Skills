---
name: mcp-multiroundtrip-input-flow-review
description: "Use when designing or testing an MCP request that may pause to ask the client or user for additional input before completing, such as a tool call that needs approval or a prompt/resource that needs a selection to review InputRequiredResult, input requests/responses, opaque request state, retry IDs, consent, replay handling, and supported request types. Success means the retry is bound to the original request, user decisions remain explicit, and incomplete or repeated input cannot cause an unintended action."
---

# MCP Multi Round-Trip Input Flow Review

## Overview

This skill applies when designing or testing an MCP request that may pause to ask the client or user for additional input before completing, such as a tool call that needs approval or a prompt/resource that needs a selection. Its intended outcome is to review InputRequiredResult, input requests/responses, opaque request state, retry IDs, consent, replay handling, and supported request types.

## When to Use

### Preserved source section: When to Use

Use this workflow for the current MCP Multi Round-Trip Requests (MRTR) pattern when a server needs client/user input while processing a request. It is especially useful for elicitation and approval flows; it is not a general long-running job lifecycle review.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Source boundary statements from: Workflow

2. **Validate the server response.** Ensure `inputRequests` identifiers are unique within the request and each value is a supported request type. An `InputRequiredResult` must include at least one of `inputRequests` or `requestState`; do not return it for an unsupported client method.
3. **Protect request state.** Treat `requestState` as opaque to the client and attacker-controlled when it returns to the server. The client must echo it exactly when supplied and must not parse or alter it. The server should protect integrity/confidentiality as needed, bind it to the operation and principal, set expiry, and enforce one-time use where required.
4. **Preserve explicit user control.** Present the request in context, disclose what data or action depends on the answer, allow refusal/cancellation, and never let the request itself authorize a destructive or external action. Do not use elicitation to solicit passwords or API secrets.
5. **Retry safely.** Send a new JSON-RPC request ID on retry, pair each response to the matching request identifier, and avoid replaying previously accepted answers. Do not attach request state or input responses to a different parallel operation.

### Source boundary statements from: Safety and Stop Conditions

Do not treat user-supplied or model-generated input as trusted authorization. Do not place credentials or sensitive personal data in `requestState`, logs, or prompts unless the approved design requires it and protects it. Stop if the client cannot present the requested input safely or distinguish refusal from acceptance.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs and Boundaries

Record the protocol version, original method, requested input types, data sensitivity, user-consent policy, request-state design, retry limits, and side effects that may occur after resumption. In current revisions, only supported methods such as `prompts/get`, `resources/read`, and `tools/call` can return `InputRequiredResult`; verify the latest specification before relying on that list.

## Instructions

### Preserved source section: Workflow

1. **Map the round trip.** Document the initial client request, why more input is needed, the user-facing question, input response shape, retry, and final result. For new implementations, prefer supported elicitation patterns; treat deprecated client features as legacy compatibility only.
2. **Validate the server response.** Ensure `inputRequests` identifiers are unique within the request and each value is a supported request type. An `InputRequiredResult` must include at least one of `inputRequests` or `requestState`; do not return it for an unsupported client method.
3. **Protect request state.** Treat `requestState` as opaque to the client and attacker-controlled when it returns to the server. The client must echo it exactly when supplied and must not parse or alter it. The server should protect integrity/confidentiality as needed, bind it to the operation and principal, set expiry, and enforce one-time use where required.
4. **Preserve explicit user control.** Present the request in context, disclose what data or action depends on the answer, allow refusal/cancellation, and never let the request itself authorize a destructive or external action. Do not use elicitation to solicit passwords or API secrets.
5. **Retry safely.** Send a new JSON-RPC request ID on retry, pair each response to the matching request identifier, and avoid replaying previously accepted answers. Do not attach request state or input responses to a different parallel operation.
6. **Test failure and replay paths.** Cover refusal, malformed response, missing state, state tampering, duplicate response, timeout, lost connection, and repeated retry. Confirm no side effect occurs before required input and approval are complete.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Workflow

3. **Protect request state.** Treat `requestState` as opaque to the client and attacker-controlled when it returns to the server. The client must echo it exactly when supplied and must not parse or alter it. The server should protect integrity/confidentiality as needed, bind it to the operation and principal, set expiry, and enforce one-time use where required.

### Source conditional guidance from: Safety and Stop Conditions

Do not treat user-supplied or model-generated input as trusted authorization. Do not place credentials or sensitive personal data in `requestState`, logs, or prompts unless the approved design requires it and protects it. Stop if the client cannot present the requested input safely or distinguish refusal from acceptance.

## Tools and Resources

### Preserved source section: Topic Provenance

Independently authored. The current MCP MRTR and related method references informed topic discovery only; no upstream skill text or examples were copied.

- [Multi Round-Trip Requests](https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/mrtr)
- [Tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)
- [Resources](https://modelcontextprotocol.io/specification/2026-07-28/server/resources)
- [Prompts](https://modelcontextprotocol.io/specification/2026-07-28/server/prompts)

## Output Format

Not specified in source skill.

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Edge Cases and Recovery

### Source edge/failure guidance from: Workflow

6. **Test failure and replay paths.** Cover refusal, malformed response, missing state, state tampering, duplicate response, timeout, lost connection, and repeated retry. Confirm no side effect occurs before required input and approval are complete.

### Source edge/failure guidance from: Acceptance Evidence

The test record contains the method/version, input request and response schema, consent surface, state handling, retry identifiers, replay behavior, and failure outcomes. Approval is tied to the specific action and parameters, not merely to an earlier request for information.

## Stop Conditions

### Preserved source section: Safety and Stop Conditions

Do not treat user-supplied or model-generated input as trusted authorization. Do not place credentials or sensitive personal data in `requestState`, logs, or prompts unless the approved design requires it and protects it. Stop if the client cannot present the requested input safely or distinguish refusal from acceptance.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Preserved source section: Acceptance Evidence

The test record contains the method/version, input request and response schema, consent surface, state handling, retry identifiers, replay behavior, and failure outcomes. Approval is tied to the specific action and parameters, not merely to an earlier request for information.
