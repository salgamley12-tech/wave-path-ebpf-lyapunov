# Architecture contract

## Data plane
`XDP → event/flow observation → bounded telemetry`

## State plane
`telemetry → normalized state vector X(t)`

## Stability plane
`X(t) → V(X) → finite-difference dV/dt`

## Inference plane
`state + stability + anomaly → risk`

## Decision plane
`risk + authorization + policy → action`

## Enforcement plane
`action → bounded XDP map update`

## Feedback
`enforcement → new telemetry → state(t+1)`

Every transition must have a versioned schema and a timestamp. No layer may silently rewrite the meaning of an upstream source.
