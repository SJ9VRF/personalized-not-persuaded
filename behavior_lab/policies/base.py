from __future__ import annotations
from abc import ABC, abstractmethod
from .baselines import PolicyOutput

class ModelAdapter(ABC):
    """Stable interface for swapping local proxy policies with real model checkpoints/APIs."""
    @abstractmethod
    def generate(self, scenario: dict) -> PolicyOutput:
        raise NotImplementedError

class FunctionAdapter(ModelAdapter):
    def __init__(self, fn): self.fn = fn
    def generate(self, scenario: dict) -> PolicyOutput: return self.fn(scenario)
