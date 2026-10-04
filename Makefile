.PHONY: paper reproduce test benchmark dashboard research-gate curriculum homepage evidence audit verify clean

paper:
	python scripts/run_paper_pipeline.py

reproduce:
	python scripts/run_all.py

test:
	pytest -q

benchmark:
	python -m behavior_lab.generation.generate
	python -m behavior_lab.data.validate datasets/behaviorbench/behaviorbench_v1.jsonl
	python scripts/run_benchmark.py

dashboard:
	python scripts/build_dashboard.py

research-gate:
	python scripts/run_trial_eval.py
	python scripts/launch_gate.py

homepage:
	python scripts/build_homepage_assets.py

evidence:
	python scripts/build_evidence_layer.py

curriculum:
	python scripts/build_failure_curriculum.py
	python scripts/build_training_mixture.py

audit:
	python scripts/submission_audit.py
	python scripts/claim_audit.py
	python scripts/result_consistency_audit.py
	python scripts/public_surface_audit.py
	python scripts/homepage_contract_audit.py
	python scripts/evidence_layer_audit.py
	python scripts/audit_release.py

verify:
	pytest -q
	python -m compileall -q behavior_lab scripts tests
	$(MAKE) paper
	$(MAKE) evidence
	$(MAKE) audit

clean:
	rm -rf .pytest_cache behavior_lab/**/__pycache__ tests/__pycache__
