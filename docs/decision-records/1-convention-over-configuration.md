# Convention over configuration

## Context
Too many configuration options creates configuration sprawl, burdening operations teams and wasting their time.

As more configuration options are added, project complexity explodes, as configuration options have to loaded, parsed, validated, utilized, tested, etc. Configuration options also have to be documented, including their behaviours and interactions with other configuration options.

## Decision
We will minimize the number of configuration options available on all interfaces by making opinionated decisions about how certain interfaces should behave, while ensuring that the behaviour of those interfaces satisfies the majority of the consumers of this library.

## Consequences
Interfaces will have fewer configuration options, resulting in lowered burden on developers and operations teams.

Some users of this library will be unsatisfied by certain decisions. Great care will have to be taken to ensure that their requirements are justifiable enough to introduce another configuration option to this library.
