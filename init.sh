#!/bin/bash

set -euo pipefail

create_architecture() {
    mkdir -p $1/switches/access/marketing/interfaces
    mkdir -p $1/switches/access/it/interfaces
    mkdir -p $1/switches/access/direction/interfaces
    mkdir -p $1/switches/backbone/interfaces
    mkdir -p $1/hosts
    mkdir -p $1/routers/active
}

create_architecture $1