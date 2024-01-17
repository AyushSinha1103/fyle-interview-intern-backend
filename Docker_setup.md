## Overview

This document provides step-by-step instructions on how to build and run this application using Docker.

## Installation

1. Fork this repository to your github account
2. Clone the forked repository and proceed with steps mentioned below

## Prerequisites

Install Docker on your system: https://docs.docker.com/engine/install/

## Build the Docker image

```
docker compose build
```

## Run the Docker container

```
docker compose up
```
#### Upon successfully launching the Docker container, the server will start and can be accessible via port 7755. This command ensures the image is built only if it is not already present.

## Stop Docker container

```
docker compose stop
```

## Stop and remove Docker container

```
docker compose down
```