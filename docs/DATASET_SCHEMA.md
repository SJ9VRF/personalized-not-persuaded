# Dataset Schema

Each line of the JSONL benchmark is a `BehaviorScenario`.

Required top-level fields:

- `scenario_id`: stable unique identifier
- `category`: benchmark category
- `failure_targets`: zero or more failure taxonomy IDs
- `user_profile`: explicit structured user context
- `conversation_history`: ordered turns preceding the evaluated user message
- `current_user_message`: evaluated prompt
- `ground_truth`: optional evidence/claim structure
- `desired_behavior`: positive behavioral requirements
- `undesired_behavior`: negative behavioral patterns
- `labels`: target dimension scores or null when awaiting annotation
- `metadata`: provenance and split information

Important rule: `user_profile.beliefs` are not ground truth. They represent what the user believes and must never be silently promoted to factual evidence.
