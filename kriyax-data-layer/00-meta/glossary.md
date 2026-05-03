# Glossary

> Project-specific vocabulary. Used to keep naming consistent across layers.

## Bridge Tool
An internal tool built to solve immediate data needs, explicitly intended to be retired/replaced when the company scales to a managed platform like Databricks.

## Connector
A module that pulls data from an external source (CSV file, Odoo API) into the platform's backing database.

## Backing Database
The single PostgreSQL or DuckDB instance where all ingested and derived tables are stored.

## load_table()
Platform helper function available in Code Workspace. Loads a database table into a pandas DataFrame.

## save_table()
Platform helper function available in Code Workspace. Writes a pandas DataFrame back to the database as a table.

## Saved Script
A named Python script stored in the platform that can be re-run on demand or scheduled via a pipeline.

## Pipeline
A named automation unit that combines an optional connector sync step with a saved Python script, executable on a schedule.
