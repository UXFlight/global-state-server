#!/bin/bash

set -e

echo "Cleaning log directories..."

rm -rf logs/pilot-logs/*
rm -rf logs/atc-logs/*

echo "Logs cleaned: pilot-logs and atc-logs"
