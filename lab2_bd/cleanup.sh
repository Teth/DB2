#!/bin/bash
pkill -9 Python
redis-cli flushall
redis-cli shutdown