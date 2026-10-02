from typing import Iterable, List, Tuple

from model.observation.observation import Observation, observe
from model.observation.reference_observation import ObservationDefinition


def run_observation(
    definition: ObservationDefinition,
    signal: Iterable[Tuple[float, float]],
    sigma: float = 0.0,
    seed: int = 7,
) -> List[Observation]:
    if not definition.variables:
        raise ValueError("observation definition has no variables")

    return observe(signal, sigma=sigma, seed=seed)
