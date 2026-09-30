---
name: mcp-http-authorization-and-registration-audit
description: "Use when auditing OAuth authorization between an MCP client, protected MCP server, and authorization server over an HTTP transport to verify protected-resource discovery, issuer binding, client registration, resource indicators, token audience, scopes, PKCE, and separation from upstream API credentials. Success means a token is accepted only for its intended MCP resource and authorization context, least privilege is demonstrable, and mismatched or overbroad credentials are rejected without leaking secrets. Check the protocol revision before relying on registration details."
---

# MCP HTTP Authorization and Registration Audit

## Overview

This skill applies when auditing OAuth authorization between an MCP client, protected MCP server, and authorization server over an HTTP transport. Its intended outcome is to verify protected-resource discovery, issuer binding, client registration, resource indicators, token audience, scopes, PKCE, and separation from upstream API credentials.

## When to Use

### Preserved source section: When to Use

Use this workflow to review an MCP HTTP authorization flow before enabling a protected remote server, changing OAuth registration, or investigating a token or issuer mismatch. It does not replace an organization’s identity-provider review or grant access to a system.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Source boundary statements from: When to Use

Use this workflow to review an MCP HTTP authorization flow before enabling a protected remote server, changing OAuth registration, or investigating a token or issuer mismatch. It does not replace an organization’s identity-provider review or grant access to a system.

### Source boundary statements from: Inputs and Boundaries

Record the MCP endpoint, client and server roles, authorization-server issuer(s), protocol revision, registration mode, requested scopes, token audience/resource, redirect URIs, credential storage, upstream APIs, and approval owner. Do not paste tokens or secrets into reports or chats; inspect redacted metadata and controlled test credentials.

### Source boundary statements from: Workflow

1. **Confirm the transport and roles.** Authorization is optional for MCP generally. For HTTP authorization, treat the MCP server as a resource server, the MCP client as an OAuth client, and the authorization server as the token issuer. Do not apply the HTTP OAuth profile to STDIO as though it were required there.
5. **Separate upstream authorization.** If the MCP server calls another API, require a separate upstream credential obtained for that API. Never forward the token received from the MCP client as an upstream bearer token. Keep credentials out of tool arguments, model context, logs, and error messages.

### Source boundary statements from: Safety and Stop Conditions

Do not enable broad scopes to work around a failed authorization flow. Never log or disclose access/refresh tokens, authorization codes, client secrets, or private user data. Stop if issuer ownership, redirect control, consent, or credential separation is uncertain.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs and Boundaries

Record the MCP endpoint, client and server roles, authorization-server issuer(s), protocol revision, registration mode, requested scopes, token audience/resource, redirect URIs, credential storage, upstream APIs, and approval owner. Do not paste tokens or secrets into reports or chats; inspect redacted metadata and controlled test credentials.

## Instructions

### Preserved source section: Workflow

1. **Confirm the transport and roles.** Authorization is optional for MCP generally. For HTTP authorization, treat the MCP server as a resource server, the MCP client as an OAuth client, and the authorization server as the token issuer. Do not apply the HTTP OAuth profile to STDIO as though it were required there.
2. **Validate protected-resource discovery.** Confirm the MCP server exposes Protected Resource Metadata with at least one `authorization_servers` entry. Test the 401 `WWW-Authenticate` metadata URL and well-known fallback. Validate issuer values and keep separate client credentials and token state for each authorization-server issuer.
3. **Review client registration.** Prefer existing pre-registration when configured; otherwise use Client ID Metadata Documents when advertised. Treat Dynamic Client Registration as a deprecated compatibility fallback, not the default for new implementations. Check exact metadata URL/client-ID match, required fields, redirect URI allowlisting, and registration binding.
4. **Bind tokens to the MCP resource.** Verify the client sends the RFC 8707 `resource` parameter in authorization and token requests. Confirm the server validates each inbound token for its intended audience and rejects tokens issued for another resource, wrong issuer, expired credentials, invalid signature, or insufficient scope.
5. **Separate upstream authorization.** If the MCP server calls another API, require a separate upstream credential obtained for that API. Never forward the token received from the MCP client as an upstream bearer token. Keep credentials out of tool arguments, model context, logs, and error messages.
6. **Exercise negative cases.** Test issuer mismatch, altered redirect URI, missing PKCE support, wrong audience, cross-user cache reuse, insufficient tool scope, token expiry, and refresh failure using isolated test identities. Record expected denial and recovery behavior.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Workflow

3. **Review client registration.** Prefer existing pre-registration when configured; otherwise use Client ID Metadata Documents when advertised. Treat Dynamic Client Registration as a deprecated compatibility fallback, not the default for new implementations. Check exact metadata URL/client-ID match, required fields, redirect URI allowlisting, and registration binding.
5. **Separate upstream authorization.** If the MCP server calls another API, require a separate upstream credential obtained for that API. Never forward the token received from the MCP client as an upstream bearer token. Keep credentials out of tool arguments, model context, logs, and error messages.

### Source conditional guidance from: Safety and Stop Conditions

Do not enable broad scopes to work around a failed authorization flow. Never log or disclose access/refresh tokens, authorization codes, client secrets, or private user data. Stop if issuer ownership, redirect control, consent, or credential separation is uncertain.

## Tools and Resources

### Preserved source section: Topic Provenance

Independently authored. The current official MCP authorization documents below informed technical topic discovery; no upstream skill text or examples were copied. Verify the active protocol revision and OAuth guidance before implementation.

- [MCP Authorization](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization)
- [Authorization Server Discovery](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization/authorization-server-discovery)
- [Client Registration](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization/client-registration)
- [Authorization Security Considerations](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization/security-considerations)

## Output Format

Not specified in source skill.

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Edge Cases and Recovery

### Source edge/failure guidance from: Workflow

2. **Validate protected-resource discovery.** Confirm the MCP server exposes Protected Resource Metadata with at least one `authorization_servers` entry. Test the 401 `WWW-Authenticate` metadata URL and well-known fallback. Validate issuer values and keep separate client credentials and token state for each authorization-server issuer.
3. **Review client registration.** Prefer existing pre-registration when configured; otherwise use Client ID Metadata Documents when advertised. Treat Dynamic Client Registration as a deprecated compatibility fallback, not the default for new implementations. Check exact metadata URL/client-ID match, required fields, redirect URI allowlisting, and registration binding.
4. **Bind tokens to the MCP resource.** Verify the client sends the RFC 8707 `resource` parameter in authorization and token requests. Confirm the server validates each inbound token for its intended audience and rejects tokens issued for another resource, wrong issuer, expired credentials, invalid signature, or insufficient scope.
5. **Separate upstream authorization.** If the MCP server calls another API, require a separate upstream credential obtained for that API. Never forward the token received from the MCP client as an upstream bearer token. Keep credentials out of tool arguments, model context, logs, and error messages.
6. **Exercise negative cases.** Test issuer mismatch, altered redirect URI, missing PKCE support, wrong audience, cross-user cache reuse, insufficient tool scope, token expiry, and refresh failure using isolated test identities. Record expected denial and recovery behavior.

### Source edge/failure guidance from: Safety and Stop Conditions

Do not enable broad scopes to work around a failed authorization flow. Never log or disclose access/refresh tokens, authorization codes, client secrets, or private user data. Stop if issuer ownership, redirect control, consent, or credential separation is uncertain.

## Stop Conditions

### Preserved source section: Safety and Stop Conditions

Do not enable broad scopes to work around a failed authorization flow. Never log or disclose access/refresh tokens, authorization codes, client secrets, or private user data. Stop if issuer ownership, redirect control, consent, or credential separation is uncertain.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Preserved source section: Acceptance Evidence

The review includes the discovery chain, issuer-to-credential mapping, registration method, redirect URI checks, requested and granted scopes, audience validation, upstream credential separation, and negative-test evidence. A successful login alone does not prove correct resource binding.
