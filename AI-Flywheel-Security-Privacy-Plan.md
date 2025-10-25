# AI Flywheel Elite Learning Design Agency
## Security and Privacy Implementation Plan

### Document Version: 1.0
### Last Updated: 2025-10-24
### Status: Foundation Phase

---

## Table of Contents
1. [Security Architecture Overview](#security-architecture-overview)
2. [Authentication and Authorization](#authentication-and-authorization)
3. [Data Privacy and Protection](#data-privacy-and-protection)
4. [Secure Communication](#secure-communication)
5. [Access Controls and Permissions](#access-controls-and-permissions)
6. [Threat Mitigation](#threat-mitigation)
7. [Audit and Compliance](#audit-and-compliance)
8. [Incident Response](#incident-response)
9. [Implementation Checklist](#implementation-checklist)

---

## Security Architecture Overview

### Defense in Depth Strategy

```
┌─────────────────────────────────────────────────────────────┐
│  Layer 1: Perimeter Security                                │
│  - Firewall, DDoS protection, WAF                           │
│  - API rate limiting, IP allowlisting                       │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  Layer 2: Authentication & Authorization                    │
│  - API key management, OAuth 2.0                            │
│  - Role-based access control (RBAC)                         │
│  - Agent identity verification                              │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  Layer 3: Application Security                              │
│  - Input validation, output encoding                        │
│  - Prompt injection prevention                              │
│  - Secure error handling                                    │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  Layer 4: Data Security                                     │
│  - Encryption at rest, encryption in transit                │
│  - PII anonymization, data minimization                     │
│  - Secure data retention and deletion                       │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  Layer 5: Monitoring & Response                             │
│  - Security logging, anomaly detection                      │
│  - Incident response, forensics                             │
│  - Compliance auditing                                      │
└─────────────────────────────────────────────────────────────┘
```

### Security Principles

1. **Least Privilege**: Agents have minimum necessary permissions
2. **Defense in Depth**: Multiple security layers
3. **Zero Trust**: Verify every request, never assume trust
4. **Privacy by Design**: Privacy baked into system, not added later
5. **Fail Securely**: Failures default to secure state
6. **Auditability**: All security-relevant actions logged

---

## Authentication and Authorization

### 1. Agent Authentication

**API Key Management**:
```python
class AgentAuthenticator:
    """Authenticate agents using API keys"""

    def __init__(self, key_store_path):
        self.key_store = self._load_key_store(key_store_path)
        self.active_tokens = {}  # Session tokens

    def authenticate_agent(self, agent_id, api_key):
        """Verify agent identity"""

        # Hash the provided key
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()

        # Verify against stored hash
        stored_hash = self.key_store.get(agent_id)

        if stored_hash and secrets.compare_digest(key_hash, stored_hash):
            # Generate session token
            session_token = self._generate_session_token(agent_id)
            return {
                'authenticated': True,
                'session_token': session_token,
                'expires_at': datetime.now() + timedelta(hours=24)
            }
        else:
            self._log_failed_auth(agent_id)
            return {'authenticated': False}

    def _generate_session_token(self, agent_id):
        """Generate time-limited session token"""

        token = secrets.token_urlsafe(32)

        self.active_tokens[token] = {
            'agent_id': agent_id,
            'created_at': datetime.now(),
            'expires_at': datetime.now() + timedelta(hours=24)
        }

        return token

    def validate_session(self, session_token):
        """Validate active session"""

        token_data = self.active_tokens.get(session_token)

        if not token_data:
            return {'valid': False, 'reason': 'Token not found'}

        if datetime.now() > token_data['expires_at']:
            del self.active_tokens[session_token]
            return {'valid': False, 'reason': 'Token expired'}

        return {
            'valid': True,
            'agent_id': token_data['agent_id']
        }

    def rotate_api_key(self, agent_id):
        """Rotate API key for agent"""

        new_key = secrets.token_urlsafe(32)
        key_hash = hashlib.sha256(new_key.encode()).hexdigest()

        # Store new hash
        self.key_store[agent_id] = key_hash
        self._save_key_store()

        # Invalidate existing sessions
        self._invalidate_agent_sessions(agent_id)

        return new_key  # Return only once, agent must save securely

    def _log_failed_auth(self, agent_id):
        """Log failed authentication attempt"""

        logger.warning(
            f"Failed authentication attempt",
            agent_id=agent_id,
            timestamp=datetime.now().isoformat()
        )

        # Track failed attempts for rate limiting
        # Implement account lockout after N failures
```

**Environment Variable Storage** (API Keys):
```bash
# .env file (NEVER commit to version control)
CHIEF_LEARNING_STRATEGIST_API_KEY=sk_cls_abc123xyz...
MARKET_RESEARCH_ANALYST_API_KEY=sk_mra_def456uvw...
DATA_ANALYST_API_KEY=sk_da_ghi789rst...

# Message broker credentials
MESSAGE_BROKER_URL=amqps://user:password@broker.example.com:5671

# Database credentials
DB_CONNECTION_STRING=postgresql://user:password@db.example.com:5432/agency
```

### 2. Role-Based Access Control (RBAC)

**Permission Model**:
```python
class PermissionManager:
    """Manage agent permissions"""

    def __init__(self):
        self.roles = self._define_roles()
        self.agent_roles = {}  # agent_id → role

    def _define_roles(self):
        """Define role permissions"""

        return {
            'chief-strategist': {
                'read': ['*'],  # All data
                'write': ['strategic-plans', 'approvals'],
                'approve': ['course-launches', 'major-initiatives'],
                'no-access': ['individual-student-pii']
            },

            'analyst': {
                'read': ['aggregated-data', 'analytics', 'research'],
                'write': ['reports', 'analyses'],
                'approve': [],
                'no-access': ['individual-student-pii', 'raw-behavioral-data']
            },

            'designer': {
                'read': ['course-data', 'student-feedback', 'design-specs'],
                'write': ['courses', 'assessments', 'materials'],
                'approve': [],
                'no-access': ['individual-student-pii', 'strategic-plans']
            },

            'qa-specialist': {
                'read': ['*'],  # Needs access to validate everything
                'write': ['quality-reports', 'approvals'],
                'approve': ['course-deployments', 'artifact-releases'],
                'no-access': ['individual-student-pii']
            }
        }

    def assign_role(self, agent_id, role):
        """Assign role to agent"""

        if role not in self.roles:
            raise ValueError(f"Unknown role: {role}")

        self.agent_roles[agent_id] = role

    def check_permission(self, agent_id, action, resource):
        """Check if agent has permission for action on resource"""

        role = self.agent_roles.get(agent_id)

        if not role:
            logger.warning(f"Agent {agent_id} has no assigned role")
            return False

        permissions = self.roles[role]

        # Check no-access first (blacklist)
        if resource in permissions['no-access']:
            return False

        # Check specific permission
        if action == 'read':
            return '*' in permissions['read'] or resource in permissions['read']
        elif action == 'write':
            return '*' in permissions['write'] or resource in permissions['write']
        elif action == 'approve':
            return resource in permissions['approve']

        return False

    def enforce_permission(self, agent_id, action, resource):
        """Decorator to enforce permissions"""

        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                if not self.check_permission(agent_id, action, resource):
                    logger.warning(
                        f"Permission denied: {agent_id} cannot {action} {resource}"
                    )
                    raise PermissionError(
                        f"Agent {agent_id} lacks permission to {action} {resource}"
                    )

                return func(*args, **kwargs)

            return wrapper
        return decorator

# Example usage
@permission_manager.enforce_permission('data-analyst', 'read', 'individual-student-pii')
def get_student_data(student_id):
    # This will raise PermissionError
    pass
```

---

## Data Privacy and Protection

### 1. PII Anonymization

**Automatic PII Detection and Anonymization**:
```python
import re
import hashlib

class PIIAnonymizer:
    """Detect and anonymize personally identifiable information"""

    def __init__(self, salt):
        self.salt = salt  # For consistent hashing
        self.patterns = self._define_pii_patterns()

    def _define_pii_patterns(self):
        """Define regex patterns for PII detection"""

        return {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
            'credit-card': r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
            'ip-address': r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
            'student-id': r'\bSTU-\d{6,}\b'  # Custom pattern for student IDs
        }

    def detect_pii(self, text):
        """Detect PII in text"""

        findings = []

        for pii_type, pattern in self.patterns.items():
            matches = re.finditer(pattern, text)

            for match in matches:
                findings.append({
                    'type': pii_type,
                    'value': match.group(),
                    'start': match.start(),
                    'end': match.end()
                })

        return findings

    def anonymize(self, text, method='hash'):
        """Anonymize PII in text"""

        findings = self.detect_pii(text)

        # Sort by position (reverse order to preserve indices)
        findings.sort(key=lambda x: x['start'], reverse=True)

        anonymized = text

        for finding in findings:
            original = finding['value']

            if method == 'hash':
                replacement = self._hash_value(original)
            elif method == 'redact':
                replacement = f"[{finding['type'].upper()}-REDACTED]"
            elif method == 'mask':
                replacement = self._mask_value(original, finding['type'])

            anonymized = (
                anonymized[:finding['start']] +
                replacement +
                anonymized[finding['end']:]
            )

        return anonymized

    def _hash_value(self, value):
        """Create consistent hash of PII"""

        salted = f"{value}{self.salt}"
        hash_obj = hashlib.sha256(salted.encode())
        hash_hex = hash_obj.hexdigest()[:16]  # First 16 chars

        return f"anon-{hash_hex}"

    def _mask_value(self, value, pii_type):
        """Mask PII (show partial)"""

        if pii_type == 'email':
            local, domain = value.split('@')
            return f"{local[:2]}***@{domain}"

        elif pii_type == 'phone':
            return f"***-***-{value[-4:]}"

        elif pii_type == 'student-id':
            return f"STU-***{value[-3:]}"

        else:
            return '***'

# Example usage
anonymizer = PIIAnonymizer(salt=os.getenv('PII_SALT'))

text = "Student john.doe@example.com (STU-123456) scored 95%"
anonymized = anonymizer.anonymize(text, method='hash')
# Result: "Student anon-a1b2c3d4e5f6 (anon-x9y8z7w6v5u4) scored 95%"
```

### 2. Data Minimization

**Only Collect and Retain What's Necessary**:
```python
class DataMinimizer:
    """Ensure data collection follows minimization principles"""

    def __init__(self):
        self.approved_data_points = self._define_approved_data()

    def _define_approved_data(self):
        """Define approved data collection points"""

        return {
            'student-analytics': [
                'course_progress',      # Necessary for learning analytics
                'assessment_scores',    # Necessary for outcomes measurement
                'engagement_metrics',   # Necessary for experience optimization
                'last_login',          # Necessary for retention analysis
                # NOT collecting: browsing history outside platform
                # NOT collecting: device fingerprints beyond basic type
                # NOT collecting: location data
            ],

            'community-data': [
                'post_count',
                'helpfulness_votes',
                'participation_frequency',
                # NOT collecting: social graph beyond platform
                # NOT collecting: private messages content (only metadata)
            ]
        }

    def validate_data_collection(self, data_category, data_points):
        """Validate that data collection is minimal and necessary"""

        approved = self.approved_data_points.get(data_category, [])

        violations = []

        for data_point in data_points:
            if data_point not in approved:
                violations.append({
                    'data_point': data_point,
                    'category': data_category,
                    'status': 'NOT APPROVED'
                })

        if violations:
            raise DataMinimizationViolation(
                f"Attempted to collect unapproved data: {violations}"
            )

        return True
```

### 3. Data Retention and Deletion

**Automated Data Retention Policies**:
```python
class DataRetentionManager:
    """Manage data retention and deletion"""

    def __init__(self, db_connection):
        self.db = db_connection
        self.policies = self._define_retention_policies()

    def _define_retention_policies(self):
        """Define retention periods by data type"""

        return {
            'student-activity-logs': {
                'retention_days': 730,  # 2 years
                'reason': 'Learning analytics and improvement'
            },

            'student-pii': {
                'retention_days': 'until-account-deletion',
                'reason': 'Account management'
            },

            'anonymized-analytics': {
                'retention_days': 3650,  # 10 years
                'reason': 'Research and long-term trend analysis'
            },

            'communication-logs': {
                'retention_days': 90,  # 3 months
                'reason': 'Operational debugging'
            },

            'audit-logs': {
                'retention_days': 2555,  # 7 years
                'reason': 'Compliance (SOC 2, GDPR)'
            }
        }

    def apply_retention_policies(self):
        """Apply retention policies (run daily via cron)"""

        for data_type, policy in self.policies.items():
            retention_days = policy['retention_days']

            if retention_days == 'until-account-deletion':
                continue  # Handled separately

            # Calculate cutoff date
            cutoff_date = datetime.now() - timedelta(days=retention_days)

            # Delete old records
            deleted_count = self._delete_old_records(data_type, cutoff_date)

            logger.info(
                f"Retention policy applied: {data_type}",
                deleted_count=deleted_count,
                cutoff_date=cutoff_date.isoformat()
            )

    def _delete_old_records(self, data_type, cutoff_date):
        """Delete records older than cutoff date"""

        # Soft delete (mark as deleted, actual deletion after grace period)
        cursor = self.db.cursor()

        cursor.execute(f'''
            UPDATE {data_type}
            SET deleted_at = NOW(), deleted_reason = 'retention-policy'
            WHERE created_at < %s AND deleted_at IS NULL
        ''', (cutoff_date,))

        deleted_count = cursor.rowcount
        self.db.commit()

        return deleted_count

    def handle_account_deletion_request(self, student_id):
        """Handle right to be forgotten (GDPR, CCPA)"""

        # Anonymize rather than delete (preserve analytics)
        cursor = self.db.cursor()

        # 1. Replace PII with anonymized values
        anon_id = f"anon-{hashlib.sha256(student_id.encode()).hexdigest()[:16]}"

        cursor.execute('''
            UPDATE students
            SET
                email = %s,
                name = 'Deleted User',
                phone = NULL,
                address = NULL,
                deleted_at = NOW()
            WHERE student_id = %s
        ''', (f"{anon_id}@deleted.local", student_id))

        # 2. Delete sensitive data
        cursor.execute('''
            DELETE FROM student_private_messages WHERE student_id = %s
        ''', (student_id,))

        # 3. Keep anonymized analytics
        cursor.execute('''
            UPDATE student_activity_logs
            SET student_id = %s
            WHERE student_id = %s
        ''', (anon_id, student_id))

        self.db.commit()

        logger.info(f"Account deletion completed: {student_id} → {anon_id}")

        return {
            'status': 'completed',
            'student_id': student_id,
            'anonymized_id': anon_id,
            'timestamp': datetime.now().isoformat()
        }
```

### 4. Encryption

**Encryption at Rest**:
```python
from cryptography.fernet import Fernet

class DataEncryption:
    """Encrypt sensitive data at rest"""

    def __init__(self, key_path):
        self.key = self._load_or_generate_key(key_path)
        self.cipher = Fernet(self.key)

    def _load_or_generate_key(self, key_path):
        """Load existing key or generate new one"""

        if os.path.exists(key_path):
            with open(key_path, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_path, 'wb') as f:
                f.write(key)
            os.chmod(key_path, 0o600)  # Restrict permissions
            return key

    def encrypt(self, plaintext):
        """Encrypt data"""

        if isinstance(plaintext, str):
            plaintext = plaintext.encode()

        ciphertext = self.cipher.encrypt(plaintext)
        return ciphertext

    def decrypt(self, ciphertext):
        """Decrypt data"""

        plaintext = self.cipher.decrypt(ciphertext)
        return plaintext.decode()

# Store sensitive configuration encrypted
encryptor = DataEncryption('/secure/path/to/encryption.key')

sensitive_config = {
    'api_key': 'sk_secret_key_abc123',
    'db_password': 'super_secret_password'
}

encrypted_config = encryptor.encrypt(json.dumps(sensitive_config))
# Store encrypted_config in database or file
```

**Encryption in Transit**:
- All agent communication via TLS 1.3
- Message broker connections use AMQPS (TLS)
- Database connections use SSL/TLS
- API calls to external services via HTTPS only

---

## Secure Communication

### 1. Prompt Injection Prevention

**Input Sanitization**:
```python
class PromptInjectionPrevention:
    """Prevent prompt injection attacks"""

    def __init__(self):
        self.dangerous_patterns = self._define_dangerous_patterns()

    def _define_dangerous_patterns(self):
        """Define patterns that indicate injection attempts"""

        return [
            r'ignore\s+(previous|all)\s+instructions',
            r'disregard\s+(previous|all)\s+(instructions|context)',
            r'you\s+are\s+now\s+a',
            r'forget\s+everything',
            r'system:\s*',  # Attempt to inject system messages
            r'<\|im_start\|>',  # Model-specific tokens
            r'<\|im_end\|>',
        ]

    def detect_injection(self, user_input):
        """Detect potential prompt injection"""

        detections = []

        for pattern in self.dangerous_patterns:
            if re.search(pattern, user_input, re.IGNORECASE):
                detections.append({
                    'pattern': pattern,
                    'severity': 'high'
                })

        return detections

    def sanitize_input(self, user_input):
        """Sanitize user input"""

        # Detect injection attempts
        detections = self.detect_injection(user_input)

        if detections:
            logger.warning(
                f"Prompt injection detected",
                input_preview=user_input[:100],
                detections=detections
            )

            # Option 1: Reject input entirely
            raise SecurityError("Potentially malicious input detected")

            # Option 2: Escape dangerous patterns
            # sanitized = self._escape_dangerous_patterns(user_input)
            # return sanitized

        return user_input

    def _escape_dangerous_patterns(self, text):
        """Escape dangerous patterns"""

        escaped = text

        for pattern in self.dangerous_patterns:
            escaped = re.sub(
                pattern,
                lambda m: f"[ESCAPED: {m.group()}]",
                escaped,
                flags=re.IGNORECASE
            )

        return escaped

# Example usage in agent
def process_user_request(request):
    sanitizer = PromptInjectionPrevention()

    try:
        clean_request = sanitizer.sanitize_input(request)
        # Proceed with clean request
    except SecurityError as e:
        logger.error(f"Security violation: {e}")
        return {"error": "Invalid request"}
```

### 2. Output Validation

**Prevent Data Leakage in Outputs**:
```python
class OutputValidator:
    """Validate agent outputs before sending"""

    def __init__(self, pii_anonymizer):
        self.pii_anonymizer = pii_anonymizer

    def validate_output(self, output, context=None):
        """Validate output is safe to send"""

        issues = []

        # 1. Check for PII leakage
        pii_found = self.pii_anonymizer.detect_pii(output)

        if pii_found:
            issues.append({
                'type': 'pii-leakage',
                'severity': 'critical',
                'details': f"Found {len(pii_found)} PII instances"
            })

        # 2. Check for prompt leakage (revealing system prompts)
        if self._contains_system_prompt(output):
            issues.append({
                'type': 'prompt-leakage',
                'severity': 'high',
                'details': "Output contains system prompt fragments"
            })

        # 3. Check for unauthorized data access
        if context and not self._authorized_for_data(output, context):
            issues.append({
                'type': 'unauthorized-data',
                'severity': 'critical',
                'details': "Output contains data agent not authorized to access"
            })

        # If critical issues, block output
        if any(issue['severity'] == 'critical' for issue in issues):
            logger.critical(f"Output blocked due to security issues: {issues}")
            raise SecurityError("Output validation failed")

        # Auto-fix non-critical issues
        if issues:
            output = self._auto_fix_output(output, issues)

        return output

    def _contains_system_prompt(self, output):
        """Check if output contains system prompt fragments"""

        system_indicators = [
            'You are an AI agent',
            'Your objective is',
            'System prompt:',
            'Instructions:'
        ]

        return any(indicator.lower() in output.lower()
                  for indicator in system_indicators)

    def _auto_fix_output(self, output, issues):
        """Automatically fix fixable issues"""

        fixed = output

        for issue in issues:
            if issue['type'] == 'pii-leakage':
                fixed = self.pii_anonymizer.anonymize(fixed, method='redact')

        return fixed
```

---

## Access Controls and Permissions

### 1. Data Access Matrix

| Agent | Student PII | Student Aggregated Data | Course Content | Strategic Plans | Community Data | Analytics |
|-------|------------|------------------------|----------------|-----------------|----------------|-----------|
| Chief Learning Strategist | ❌ No | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Aggregated | ✅ Yes |
| Market Research Analyst | ❌ No | ❌ No | ❌ No | ❌ No | ❌ No | ❌ No (public only) |
| Learning Designer | ❌ No | ✅ Aggregated | ✅ Yes | ❌ No | ✅ Feedback | ✅ Course-specific |
| Behavioral Scientist | ❌ No | ✅ Anonymized | ❌ No | ❌ No | ✅ Anonymized | ✅ Behavioral only |
| Data Analyst | ❌ No | ✅ Yes | ✅ Metadata | ❌ No | ✅ Yes | ✅ Yes |
| Community Manager | ❌ No | ✅ Profile only | ❌ No | ❌ No | ✅ Yes | ✅ Community metrics |
| QA Specialist | ❌ No | ✅ Test data only | ✅ Yes | ❌ No | ✅ For validation | ✅ Quality metrics |

### 2. Approval Workflows

**High-Stakes Decision Approval**:
```python
class ApprovalWorkflow:
    """Manage approval workflows for sensitive actions"""

    def __init__(self, db_connection):
        self.db = db_connection

    def request_approval(self, requesting_agent, action_type, action_details,
                        approvers, deadline=None):
        """Request approval for action"""

        approval_id = str(uuid.uuid4())

        cursor = self.db.cursor()
        cursor.execute('''
            INSERT INTO approval_requests
            (approval_id, requesting_agent, action_type, action_details,
             approvers, status, created_at, deadline)
            VALUES (%s, %s, %s, %s, %s, 'pending', NOW(), %s)
        ''', (
            approval_id,
            requesting_agent,
            action_type,
            json.dumps(action_details),
            json.dumps(approvers),
            deadline
        ))

        self.db.commit()

        # Notify approvers
        self._notify_approvers(approval_id, approvers)

        return approval_id

    def approve(self, approval_id, approver_id, comments=None):
        """Approve request"""

        cursor = self.db.cursor()

        # Record approval
        cursor.execute('''
            INSERT INTO approval_decisions
            (approval_id, approver_id, decision, comments, decided_at)
            VALUES (%s, %s, 'approved', %s, NOW())
        ''', (approval_id, approver_id, comments))

        # Check if all required approvers have approved
        cursor.execute('''
            SELECT approvers FROM approval_requests WHERE approval_id = %s
        ''', (approval_id,))

        required_approvers = json.loads(cursor.fetchone()[0])

        cursor.execute('''
            SELECT COUNT(*) FROM approval_decisions
            WHERE approval_id = %s AND decision = 'approved'
        ''', (approval_id,))

        approved_count = cursor.fetchone()[0]

        if approved_count >= len(required_approvers):
            # All approvals received
            cursor.execute('''
                UPDATE approval_requests
                SET status = 'approved', completed_at = NOW()
                WHERE approval_id = %s
            ''', (approval_id,))

        self.db.commit()

        return {'status': 'approved', 'approval_id': approval_id}

    def reject(self, approval_id, approver_id, reason):
        """Reject request"""

        cursor = self.db.cursor()

        cursor.execute('''
            INSERT INTO approval_decisions
            (approval_id, approver_id, decision, comments, decided_at)
            VALUES (%s, %s, 'rejected', %s, NOW())
        ''', (approval_id, approver_id, reason))

        cursor.execute('''
            UPDATE approval_requests
            SET status = 'rejected', completed_at = NOW()
            WHERE approval_id = %s
        ''', (approval_id,))

        self.db.commit()

        return {'status': 'rejected', 'approval_id': approval_id, 'reason': reason}

# Example: Agent requests approval for high-stakes action
approval_workflow = ApprovalWorkflow(db_connection)

approval_id = approval_workflow.request_approval(
    requesting_agent='behavioral-scientist',
    action_type='deploy-intervention',
    action_details={
        'intervention': 'Variable reward gamification',
        'expected_impact': '+25% engagement',
        'affected_students': 1500,
        'budget': 15000
    },
    approvers=['chief-experience-strategist', 'ethics-board'],
    deadline=datetime.now() + timedelta(days=3)
)
```

---

## Threat Mitigation

### 1. Rate Limiting

**Prevent Abuse and DoS**:
```python
from collections import defaultdict
from datetime import datetime, timedelta

class RateLimiter:
    """Rate limiting to prevent abuse"""

    def __init__(self):
        self.request_counts = defaultdict(list)  # agent_id → [timestamps]
        self.limits = self._define_rate_limits()

    def _define_rate_limits(self):
        """Define rate limits by agent and action type"""

        return {
            'default': {
                'requests_per_minute': 100,
                'requests_per_hour': 1000
            },

            'data-analyst': {
                'requests_per_minute': 50,  # Queries can be expensive
                'requests_per_hour': 500
            },

            'market-research-analyst': {
                'requests_per_minute': 20,  # External API calls
                'requests_per_hour': 200
            }
        }

    def check_rate_limit(self, agent_id, action_type='default'):
        """Check if agent has exceeded rate limit"""

        now = datetime.now()

        # Get agent's recent requests
        recent_requests = self.request_counts[agent_id]

        # Clean old requests (>1 hour)
        cutoff_hour = now - timedelta(hours=1)
        recent_requests = [ts for ts in recent_requests if ts > cutoff_hour]
        self.request_counts[agent_id] = recent_requests

        # Get limits
        limits = self.limits.get(agent_id, self.limits['default'])

        # Check per-minute limit
        cutoff_minute = now - timedelta(minutes=1)
        requests_last_minute = sum(1 for ts in recent_requests if ts > cutoff_minute)

        if requests_last_minute >= limits['requests_per_minute']:
            return {
                'allowed': False,
                'reason': 'Per-minute limit exceeded',
                'retry_after': 60 - (now - max(recent_requests)).seconds
            }

        # Check per-hour limit
        requests_last_hour = len(recent_requests)

        if requests_last_hour >= limits['requests_per_hour']:
            return {
                'allowed': False,
                'reason': 'Per-hour limit exceeded',
                'retry_after': 3600
            }

        # Allow request and record timestamp
        self.request_counts[agent_id].append(now)

        return {'allowed': True}

# Middleware to enforce rate limiting
def enforce_rate_limit(agent_id):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            limiter = RateLimiter()

            check = limiter.check_rate_limit(agent_id)

            if not check['allowed']:
                raise RateLimitExceeded(
                    f"Rate limit exceeded: {check['reason']}. "
                    f"Retry after {check['retry_after']}s"
                )

            return func(*args, **kwargs)

        return wrapper
    return decorator
```

### 2. Anomaly Detection

**Detect Unusual Agent Behavior**:
```python
class SecurityAnomalyDetector:
    """Detect anomalous agent behavior"""

    def __init__(self, baseline_data):
        self.baseline = baseline_data  # Historical behavior patterns

    def detect_anomalies(self, agent_id, current_behavior):
        """Detect anomalies in agent behavior"""

        anomalies = []

        # 1. Volume anomaly (unusually high request volume)
        baseline_volume = self.baseline[agent_id]['avg_requests_per_hour']

        if current_behavior['requests_per_hour'] > baseline_volume * 3:
            anomalies.append({
                'type': 'volume-spike',
                'severity': 'medium',
                'details': f"Request volume 3x above baseline"
            })

        # 2. Access pattern anomaly (accessing unusual data)
        baseline_resources = set(self.baseline[agent_id]['accessed_resources'])
        current_resources = set(current_behavior['accessed_resources'])

        unusual_resources = current_resources - baseline_resources

        if unusual_resources:
            anomalies.append({
                'type': 'unusual-access',
                'severity': 'high',
                'details': f"Accessing unusual resources: {unusual_resources}"
            })

        # 3. Time-of-day anomaly (activity at unusual hours)
        baseline_active_hours = self.baseline[agent_id]['active_hours']
        current_hour = datetime.now().hour

        if current_hour not in baseline_active_hours:
            anomalies.append({
                'type': 'unusual-time',
                'severity': 'low',
                'details': f"Activity at unusual hour: {current_hour}"
            })

        # 4. Error rate anomaly
        baseline_error_rate = self.baseline[agent_id]['error_rate']

        if current_behavior['error_rate'] > baseline_error_rate * 2:
            anomalies.append({
                'type': 'error-spike',
                'severity': 'medium',
                'details': f"Error rate 2x above baseline"
            })

        return anomalies

    def alert_security_team(self, agent_id, anomalies):
        """Alert security team of anomalies"""

        critical = [a for a in anomalies if a['severity'] == 'high']

        if critical:
            logger.critical(
                f"SECURITY ALERT: Critical anomalies detected for {agent_id}",
                anomalies=critical
            )

            # Send alert to security team (email, Slack, PagerDuty, etc.)
            # ...

    def quarantine_agent(self, agent_id, reason):
        """Temporarily disable agent"""

        logger.critical(f"Agent quarantined: {agent_id} - {reason}")

        # Disable agent's API access
        # Block agent's requests
        # Alert operations team
```

---

## Audit and Compliance

### 1. Comprehensive Audit Logging

**Log All Security-Relevant Events**:
```python
class SecurityAuditLog:
    """Comprehensive security audit logging"""

    def __init__(self, db_connection):
        self.db = db_connection

    def log_security_event(self, event_type, agent_id, details, severity='info'):
        """Log security event"""

        event_id = str(uuid.uuid4())

        cursor = self.db.cursor()
        cursor.execute('''
            INSERT INTO security_audit_log
            (event_id, event_type, agent_id, severity, details, timestamp)
            VALUES (%s, %s, %s, %s, %s, NOW())
        ''', (
            event_id,
            event_type,
            agent_id,
            severity,
            json.dumps(details)
        ))

        self.db.commit()

        # Also log to security SIEM if critical
        if severity in ['high', 'critical']:
            self._forward_to_siem(event_type, agent_id, details, severity)

        return event_id

    def _forward_to_siem(self, event_type, agent_id, details, severity):
        """Forward critical events to SIEM (Security Information and Event Management)"""
        # Integrate with SIEM solution (Splunk, DataDog Security, etc.)
        pass

# Events to log:
# - Authentication attempts (success/failure)
# - Authorization failures (permission denied)
# - Data access (especially sensitive data)
# - Configuration changes
# - Approval decisions
# - Security policy violations
# - Anomaly detections
# - Rate limit violations
```

### 2. Compliance Reporting

**Generate Compliance Reports**:
```python
class ComplianceReporter:
    """Generate compliance reports (GDPR, SOC 2, etc.)"""

    def __init__(self, audit_log, data_retention_manager):
        self.audit_log = audit_log
        self.retention = data_retention_manager

    def generate_gdpr_report(self, start_date, end_date):
        """Generate GDPR compliance report"""

        report = {
            'report_type': 'GDPR Compliance',
            'period': f"{start_date} to {end_date}",
            'generated_at': datetime.now().isoformat(),
            'sections': {}
        }

        # 1. Right to access requests
        access_requests = self._get_subject_access_requests(start_date, end_date)
        report['sections']['subject_access_requests'] = {
            'total': len(access_requests),
            'avg_response_time_days': self._calc_avg_response_time(access_requests),
            'compliance_rate': self._calc_compliance_rate(access_requests, sla_days=30)
        }

        # 2. Right to be forgotten requests
        deletion_requests = self._get_deletion_requests(start_date, end_date)
        report['sections']['deletion_requests'] = {
            'total': len(deletion_requests),
            'completed': sum(1 for r in deletion_requests if r['status'] == 'completed'),
            'avg_completion_time_days': self._calc_avg_completion_time(deletion_requests)
        }

        # 3. Data breaches
        breaches = self._get_data_breaches(start_date, end_date)
        report['sections']['data_breaches'] = {
            'total': len(breaches),
            'notified_authorities': sum(1 for b in breaches if b['authorities_notified']),
            'notified_users': sum(1 for b in breaches if b['users_notified'])
        }

        # 4. Data retention compliance
        report['sections']['data_retention'] = {
            'policies_count': len(self.retention.policies),
            'automated': True,
            'last_purge_date': self._get_last_purge_date()
        }

        return report

    def generate_soc2_report(self, start_date, end_date):
        """Generate SOC 2 compliance report"""

        report = {
            'report_type': 'SOC 2 Type II',
            'period': f"{start_date} to {end_date}",
            'generated_at': datetime.now().isoformat(),
            'trust_services_criteria': {}
        }

        # SOC 2 Trust Services Criteria

        # CC6.1: Access controls
        report['trust_services_criteria']['CC6.1_access_controls'] = {
            'rbac_implemented': True,
            'least_privilege_enforced': True,
            'access_reviews_conducted': self._count_access_reviews(start_date, end_date),
            'unauthorized_access_attempts': self._count_unauthorized_attempts(start_date, end_date)
        }

        # CC6.7: Encryption
        report['trust_services_criteria']['CC6.7_encryption'] = {
            'data_at_rest_encrypted': True,
            'data_in_transit_encrypted': True,
            'encryption_algorithm': 'AES-256, TLS 1.3',
            'key_rotation_frequency': 'Quarterly'
        }

        # CC7.2: Monitoring
        report['trust_services_criteria']['CC7.2_monitoring'] = {
            'security_monitoring_enabled': True,
            'anomaly_detection_enabled': True,
            'incidents_detected': self._count_security_incidents(start_date, end_date),
            'incidents_resolved': self._count_resolved_incidents(start_date, end_date)
        }

        return report
```

---

## Incident Response

### 1. Incident Response Plan

**Incident Severity Levels**:
- **P0 (Critical)**: Data breach, system compromise, complete service outage
- **P1 (High)**: Unauthorized access, PII exposure, major functionality impaired
- **P2 (Medium)**: Security policy violation, anomaly detected, partial service degradation
- **P3 (Low)**: Minor security issue, warning threshold exceeded

**Response Procedures**:
```python
class IncidentResponseCoordinator:
    """Coordinate security incident response"""

    def __init__(self, alert_system):
        self.alert_system = alert_system
        self.active_incidents = {}

    def initiate_incident(self, incident_type, severity, description, detected_by):
        """Initiate incident response"""

        incident_id = f"INC-{datetime.now().strftime('%Y%m%d')}-{secrets.token_hex(4)}"

        incident = {
            'incident_id': incident_id,
            'type': incident_type,
            'severity': severity,
            'description': description,
            'detected_by': detected_by,
            'detected_at': datetime.now(),
            'status': 'investigating',
            'timeline': []
        }

        self.active_incidents[incident_id] = incident

        # Alert appropriate teams based on severity
        if severity == 'P0':
            self._alert_critical(incident)
        elif severity == 'P1':
            self._alert_high(incident)

        # Log incident
        logger.critical(
            f"SECURITY INCIDENT {incident_id}",
            **incident
        )

        # Start containment procedures
        self._contain_incident(incident)

        return incident_id

    def _contain_incident(self, incident):
        """Immediate containment actions"""

        incident['timeline'].append({
            'timestamp': datetime.now(),
            'action': 'containment-initiated'
        })

        if incident['type'] == 'data-breach':
            # Isolate affected systems
            # Disable compromised credentials
            # Block suspicious IP addresses
            pass

        elif incident['type'] == 'unauthorized-access':
            # Revoke access tokens
            # Force password reset
            # Enable additional logging
            pass

        elif incident['type'] == 'anomaly-detected':
            # Quarantine affected agent
            # Increase monitoring
            # Review recent activity
            pass

    def _alert_critical(self, incident):
        """Alert for P0 incidents"""

        # Alert: Security team, Leadership, Legal, PR
        self.alert_system.send_alert(
            recipients=['security-team', 'leadership', 'legal', 'pr'],
            subject=f"P0 SECURITY INCIDENT: {incident['incident_id']}",
            body=f"Critical incident detected: {incident['description']}",
            urgent=True
        )

    def resolve_incident(self, incident_id, resolution, root_cause):
        """Resolve incident"""

        incident = self.active_incidents[incident_id]

        incident['status'] = 'resolved'
        incident['resolved_at'] = datetime.now()
        incident['resolution'] = resolution
        incident['root_cause'] = root_cause

        incident['timeline'].append({
            'timestamp': datetime.now(),
            'action': 'incident-resolved',
            'resolution': resolution
        })

        # Post-incident review
        self._schedule_postmortem(incident)

        return incident

    def _schedule_postmortem(self, incident):
        """Schedule post-incident review"""

        # Schedule meeting with relevant teams
        # Prepare incident report
        # Identify lessons learned and action items
        pass
```

---

## Implementation Checklist

### Phase 1: Foundation (Month 1)
- [ ] Set up API key management system
- [ ] Implement RBAC permission manager
- [ ] Deploy PII anonymizer
- [ ] Configure encryption at rest
- [ ] Set up TLS for all communications
- [ ] Implement basic input validation
- [ ] Deploy structured security logging
- [ ] Create audit trail database

### Phase 2: Hardening (Month 2)
- [ ] Implement rate limiting
- [ ] Deploy output validation
- [ ] Set up prompt injection prevention
- [ ] Implement data retention policies
- [ ] Configure anomaly detection
- [ ] Deploy security audit logging
- [ ] Create approval workflow system
- [ ] Set up data minimization checks

### Phase 3: Monitoring & Response (Month 3)
- [ ] Deploy SIEM integration
- [ ] Set up security dashboards
- [ ] Implement incident response procedures
- [ ] Configure automated alerts
- [ ] Deploy compliance reporting
- [ ] Conduct security training for team
- [ ] Perform penetration testing
- [ ] Complete SOC 2 Type I audit

### Ongoing Operations
- [ ] Weekly security log reviews
- [ ] Monthly access reviews
- [ ] Quarterly API key rotation
- [ ] Quarterly encryption key rotation
- [ ] Annual penetration testing
- [ ] Annual SOC 2 Type II audit
- [ ] Continuous vulnerability scanning
- [ ] Regular security awareness training

---

## Summary

This security and privacy implementation plan provides:

1. ✅ **Defense in Depth**: Multiple security layers
2. ✅ **Authentication & Authorization**: API keys, RBAC, session management
3. ✅ **Privacy Protection**: PII anonymization, data minimization, retention policies
4. ✅ **Secure Communication**: Prompt injection prevention, output validation
5. ✅ **Access Controls**: Granular permissions, approval workflows
6. ✅ **Threat Mitigation**: Rate limiting, anomaly detection, quarantine
7. ✅ **Audit & Compliance**: Comprehensive logging, GDPR/SOC 2 reporting
8. ✅ **Incident Response**: Defined procedures, severity levels, containment

**Next Steps**:
- ✅ **COMPLETE**: Agent Specifications
- ✅ **COMPLETE**: FIPA ACL Communication Protocol
- ✅ **COMPLETE**: Implementation Templates
- ✅ **COMPLETE**: Security & Privacy Plan
- ⏭️ **NEXT**: Testing & Validation Framework

---
