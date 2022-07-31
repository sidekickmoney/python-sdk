# Externally configurable interfaces

## Context
Exposing configuration options in applications is expensive work for the developer. Configuration needs to be read in, parsed, sanitized, validated, etc. This naturally leads to fewer configuration options available for operations teams to tune as developers become hesitant exposing too many options. As a result, common operations/platform efforts such as moving to a different secrets store, or utilizing a newly standardized tracing protocol in all your applications requires code change, and strenuous collaboration between developers and operations.

## Decision
We will create externally configurable interfaces by using the `config` package for all interface.

## Consequences
All interfaces (logging, hashing, crypto, etc) can be configured externally such as over environment variables, AWS Parameter Store, and any other config sources that the `config` package supports.

All interfaces will benefit from other features supported by the `config` package, such as hot config reloading, fetching config from secrets stores, etc.

If absolutely required, as an escape hatch, interface consumers can configure packages by setting environment variables before importing any package.
