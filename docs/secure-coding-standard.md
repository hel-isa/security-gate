# Secure Coding Standard (ASVS-inspired, v1)

## Purpose
This baseline defines minimum secure coding expectations for pull requests and mainline merges.

## Core Controls
1. **Input Validation**
   - Validate all external input.
   - Prefer allow-lists over deny-lists.

2. **Output Encoding**
   - Encode output by context (HTML, JSON, SQL, shell).
   - Avoid direct concatenation for dynamic execution contexts.

3. **Authentication and Session Hygiene**
   - Enforce strong authentication patterns.
   - Never hardcode credentials or tokens.

4. **Access Control**
   - Apply least privilege at API, service, and data layers.
   - Explicitly validate authorization checks server-side.

5. **Cryptography**
   - Use vetted libraries and modern algorithms.
   - Do not implement custom cryptography.

6. **Dependency and Supply Chain Security**
   - Pin and review dependencies.
   - Resolve known vulnerabilities before release.

7. **Logging and Error Handling**
   - Log security-relevant events.
   - Avoid exposing stack traces/secrets in user-facing errors.

8. **Secure Defaults**
   - Deny by default.
   - Disable unsafe features unless explicitly needed.

## Pull Request Expectations
- Include security impact notes in each PR.
- Confirm whether new secrets, dependencies, or privileged paths were introduced.
- Address or justify scanner findings before merge.
