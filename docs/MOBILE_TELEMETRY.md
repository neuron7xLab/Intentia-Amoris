# Mobile and Telemetry Bridge

Intentia can receive phone/wearable data through `POST /telemetry`.

## Sources

```text
healthkit
google_fit
garmin
homeassistant
manual
```

## Metrics

Recommended stable metrics:

```text
steps
sleep_hours
hrv_ms
resting_hr
active_energy
screen_minutes
mindful_minutes
training_load
```

## Evidence levels

```text
measured   direct device/lab measurement
inferred   derived from behavior
unknown    unavailable
```

## Rule

Telemetry can contradict a message gently, never aggressively.

Allowed:

```text
"Your message says calm, but low sleep + low HRV suggests high load. Treat this as a reason to slow down."
```

Forbidden:

```text
"You are lying."
```
